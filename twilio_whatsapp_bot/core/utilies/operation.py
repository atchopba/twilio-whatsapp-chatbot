#!/usr/bin/python
from twilio_whatsapp_bot.core.db.db import DB
from twilio_whatsapp_bot.core.db.user_activities import UserActivities
from twilio_whatsapp_bot.core.helpers import check_noun, check_number, \
    check_phonenumber, check_str, check_email, get_logger
from twilio_whatsapp_bot.core.utilies.functions import geolocate_user, \
    geolocate_place_from_user, get_list_days_to_reserve, generate_token
from typing import Any


OP_TYPE_OUT = "out"
OP_TYPE_IN = "in"
OP_TYPE_SAVE = "save"
OP_TYPE_MAP = "map"
OP_TYPE_IF = "if"

OP_TYPE_LIST = {
    OP_TYPE_OUT: OP_TYPE_OUT,
    OP_TYPE_IN: OP_TYPE_IN,
    OP_TYPE_SAVE: OP_TYPE_SAVE,
    OP_TYPE_MAP: OP_TYPE_MAP,
    OP_TYPE_IF: OP_TYPE_IF
}

OP_CHECK_NOUN = "check_noun"
OP_CHECK_STR = "check_str"
OP_CHECK_NUMBER = "check_number"
OP_CHECK_PHONENUMBER = "check_phonenumber"
OP_CHECK_CITY = "check_city"
OP_CHECK_EMAIL = "check_email"
OP_GENERATE_QRCODE = "generate_qrcode"
OP_SELECT = "select"
OP_CALENDAR_ADD = "calendar_add"
OP_CALENDAR_LIST_DAYS_2_RESERVE = "calendar_list_days_2_reserve"

OP_LIST = {
    OP_CHECK_CITY,
    OP_CHECK_NOUN,
    OP_CHECK_NUMBER,
    OP_CHECK_PHONENUMBER,
    OP_CHECK_STR,
    OP_CHECK_EMAIL,
    OP_CALENDAR_ADD,
    OP_CALENDAR_LIST_DAYS_2_RESERVE
}

IS_OP_SELECT = False
IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
IS_OP_GENERATE_QRCODE = False


class Operation(object):

    def __init__(self):
        self.type_ = ""
        self.op_ = ""
        self.column_ = ""
        self.next_op = None
        pass

    '''
    Parse the json define in json
    @raise Exception
    '''
    def parse(self, json_) -> None:
        global IS_OP_SELECT, IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE, IS_OP_GENERATE_QRCODE # noqa
        self.type_ = json_["type"] if "type" in json_ else ""
        self.op_ = json_["op"] if "op" in json_ else ""
        self.column_ = json_["column"] if "column" in json_ else ""
        self.next_op = json_["next_op"] if "next_op" in json_ else ""
        #
        msg_1 = "is an unknown operation. Notify the system administrator"
        msg_2 = '''is an unknow operation type. Please notify the system
        administrator'''
        IS_OP_SELECT = False
        IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
        IS_OP_GENERATE_QRCODE = False
        if (self.type_ is not None
                and self.type_ in OP_TYPE_LIST
                and self.op_ is not None):
            #
            if self.type_ == OP_TYPE_OUT:
                if (self.op_.startswith(OP_SELECT) and self.column_ is not None): # noqa
                    IS_OP_SELECT = True
                elif self.op_ == OP_CALENDAR_LIST_DAYS_2_RESERVE:
                    IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = True
                elif self.op_ == OP_GENERATE_QRCODE:
                    IS_OP_GENERATE_QRCODE = True
                else:
                    IS_OP_SELECT = False
                    IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
                    IS_OP_GENERATE_QRCODE = False
            #
            elif self.type_ == OP_TYPE_IN and self.op_ in OP_LIST:
                pass
            #
            elif self.type_ == OP_TYPE_SAVE:
                pass
            #
            elif self.type_ == OP_TYPE_MAP:
                pass
            #
            else:
                raise Exception("{%s} " + msg_1, self.op_)
        #
        else:
            raise Exception("{%s} " + msg_2, self.type_)
        #
        return

    '''
    Run the operation
    @return bool
    '''
    def run(self, json_: Any, msg_2_check: str) -> bool:
        self.parse(json_)
        return_ = False
        if self.type_ == OP_TYPE_IN:
            return_ = self.run_in(json_, msg_2_check)
        elif self.type_ == OP_TYPE_OUT:
            return_ = self.run_out(None, json_)
        elif self.type_ == OP_TYPE_SAVE:
            return_ = self.run_save(json_)
        #
        return return_

    def is_empty(self, json_: Any) -> bool:
        return (json_ is None or len(json_) == 0) or (json_ and "op" not in json_) # noqa

    def is_run_in(self, json_: Any) -> bool:
        return (not self.is_empty(json_) and "type" in json_ and
                json_["type"] == OP_TYPE_IN)

    def is_run_out(self, json_: Any) -> bool:
        return (not self.is_empty(json_) and "type" in json_ and
                json_["type"] == OP_TYPE_OUT)

    def is_run_save(self, json_: Any) -> bool:
        return "type" in json_ and json_["type"] == OP_TYPE_SAVE

    def is_run_map(self, json_: Any) -> bool:
        return (not self.is_empty(json_) and "type" in json_ and
                json_["type"] == OP_TYPE_MAP)

    def is_run_if(self, json_: Any) -> bool:
        return "type" in json_ and json_["type"] == OP_TYPE_IF

    def is_run_calendar_add(self, json_: Any) -> bool:
        return (not self.is_empty(json_) and
                "type" in json_ and json_["type"] == OP_TYPE_OUT and
                "next_op" in json_ and json_["next_op"] == OP_CALENDAR_ADD)

    def run_in(self, json_: Any, msg_2_check) -> bool:
        self.parse(json_)
        return_ = False
        #
        if self.op_ == OP_CHECK_PHONENUMBER:
            return_ = check_phonenumber(msg_2_check)
        elif self.op_ == OP_CHECK_CITY:
            pass
        elif self.op_ == OP_CHECK_NUMBER:
            return_ = check_number(msg_2_check)
        elif self.op_ == OP_CHECK_STR:
            return_ = check_str(msg_2_check)
        elif self.op_ == OP_CHECK_NOUN:
            return_ = check_noun(msg_2_check)
        elif self.op_ == OP_CHECK_EMAIL:
            return_ = check_email(msg_2_check)
        # log action
        get_logger().info("Operation {0} for the message '{1}'".format(self.op_, msg_2_check)) # noqa
        #
        return return_

    def run_out(self, user_token: str, json_: Any, list_available_answers: Any) -> Any:
        global IS_OP_SELECT, IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE, IS_OP_GENERATE_QRCODE # noqa
        self.parse(json_)
        operation = json_["op"]
        return_proposal = {}
        return_array = []
        url_qrcode = None
        is_cldtr = False
        # if operation select in DB
        if IS_OP_SELECT:
            result_ = DB().select(operation)
            # log action
            get_logger().info("Operation select for user_token {} : OK".format(user_token)) # noqa
            i = 0
            for r in result_:
                return_array.append(list_available_answers[i] + ". " + r[json_["column"]]) # noqa
                return_proposal[list_available_answers[i]] = r[json_["column"]]
                i += 1
        #
        elif IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE:
            is_cldtr = IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE
            IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
            tmp_array = get_list_days_to_reserve("1") # noqa
            # log action
            get_logger().info("Operation calendar to book for user_token {} : OK".format(user_token)) # noqa
            for i in range(0, len(tmp_array)):
                return_array.append(list_available_answers[i] + ". " + tmp_array[i]) # noqa
                return_proposal[list_available_answers[i]] = tmp_array[i]
        #
        elif IS_OP_GENERATE_QRCODE:
            # call generate_qrcode method from helpers
            url_qrcode = generate_token(user_token)
            # log action
            get_logger().info("Operation generate QR-code for user_token {} : OK".format(user_token)) # noqa
            IS_OP_GENERATE_QRCODE = False
        #
        return {
            "is_calendar_list_days_to_reserve": is_cldtr, # noqa
            "proposal": return_proposal,
            "array": return_array,
            "url_qrcode": url_qrcode
        }

    def run_save(self, json_: Any, user_token: str, response_msg) -> Any:
        self.parse(json_)
        #
        UserActivities().insert_data(user_token, json_["param"], response_msg)
        # log action
        get_logger().info("Operation save for params ('{0}', '{1}')".format(user_token, response_msg)) # noqa
        #
        return {
            "param": json_["param"]
        }

    def run_map(self,
                user_token: str,
                api_key: str,
                response_msg: str,
                country: str,
                business_name: str
                ) -> Any:
        # self.parse(json_)
        get_logger().info("Start finding location for user_token {0}: {1}".format(user_token, response_msg)) # noqa
        location = geolocate_user(api_key, response_msg, country)
        get_logger().info("Locations found for the user_token " + user_token + ": ", location) # noqa
        around_user = None
        if location is not None and "lat" in location and "lng" in location:
            around_user = geolocate_place_from_user(
                api_key,
                business_name,
                location["lat"],
                location["lng"]
            )
            # log action
            get_logger().info("Search result around the user: ", around_user)
            # insert into user_activities
            UserActivities().insert_data(user_token, 'geolocate', response_msg)
        #
        return around_user

    def run_if(self, json_: Any,
               response_msg: str,
               current_question: str
               ) -> Any:
        self.parse(json_)
        tmp_tokens = current_question.split("/")
        filename = tmp_tokens[len(tmp_tokens)-1]
        choices = json_["choices"]
        filenumber = ""
        for key in choices:
            if response_msg == key:
                filenumber = choices[key]
                break
        return current_question.replace(filename, str(filenumber) + ".txt")

    def run_calendar_add(self, user_token: str, person: str,
                         event_date: str, start_time: str,
                         end_time: str) -> Any:
        # insert into user_activities
        UserActivities().insert_data(user_token, 'calendar_add_event', event_date + ' from ' + start_time + ' to ' + end_time) # noqa
        # insert into user_calendar_events
        sql = "INSERT INTO user_calendar_events (user_token, person, event_date, start_time, end_time) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(user_token, person, event_date, start_time, end_time) # noqa
        DB().insert_without_datas(sql)
        # log action
        get_logger().info("Operation calendar_add for the person '{0}' user_token {1} : OK".format(person, user_token)) # noqa
        #
        return
