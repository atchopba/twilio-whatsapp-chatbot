#!/usr/bin/python
import json
import re
import requests
from twilio_whatsapp_bot.core.db.db import DB
from twilio_whatsapp_bot.core.helpers import check_noun, check_number, \
    check_phonenumber, check_str, check_email, get_list_days_to_reserve
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
OP_SELECT = "select"
OP_CALENDAR_ADD = "calendar_add"
OP_CALENDAR_LIST_DAYS_2_RESERVE = "calendar_list_days_2_reserve"
OP_CALENDAR_LIST_USER = "calendar_list_user"
OP_CALENDAR_LIST_ALL = "calendar_list_all"
OP_CALENDAR_DELETE = "calendar_delete"

OP_LIST = {
    OP_CHECK_CITY,
    OP_CHECK_NOUN,
    OP_CHECK_NUMBER,
    OP_CHECK_PHONENUMBER,
    OP_CHECK_STR,
    OP_CHECK_EMAIL,
    OP_CALENDAR_ADD,
    OP_CALENDAR_LIST_DAYS_2_RESERVE,
    OP_CALENDAR_LIST_USER,
    OP_CALENDAR_LIST_ALL,
    OP_CALENDAR_DELETE
}

IS_OP_SELECT = False
IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False


# PATTERN_OPERATION = r"^\{\"type\"\:\s*\"[a-z0-9*\s'=_]*\"(,\s*\"[a-zA-Z*\s_]*\"\:\s*\"[a-zA-Z*\s'=_(),-;]*\")+\}$"  # noqa
# PATTERN_OPERATION =  r"^\{\"type\"\:\s*\".*?\"(,\s*\".*?\"\:\s*\".*?\")+\}$"
PATTERN_OPERATION = r"^\{\"type\"\:\s*\".*?\"(,\s*\".*?\"\:\s*((\".*?\")|(\{\".*?\"\:\s*\".*?\"(,\s*\".*?\"\:\s*\".*?\")+\})))+\}$" # noqa


def clean_operations_from_question_content(msg: str) -> str:
    tmp_ = re.sub(PATTERN_OPERATION, "", msg, 0, re.MULTILINE)
    # if tmp_ != msg:
    #    tmp_ = tmp_.replace("\n", "")
    return tmp_


def get_operations_in_bot_dialog(bot_dialog: str) -> Any:
    operations_found = ""
    tmp_bot_dialog = bot_dialog.lower()
    for match in re.finditer(PATTERN_OPERATION, tmp_bot_dialog, re.MULTILINE):
        operations_found = match.group()
        break
    return {
        'operations_found': json.loads(operations_found) if (
            operations_found != "") else "",
        'msg': clean_operations_from_question_content(bot_dialog)
    }


def geolocate_user(api_key: str, search_place: str, country: str) -> Any:
    search_place = search_place.replace("  ", " ")
    search_place += ", " + country
    search_place = search_place.replace(" ", "%20")
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ search_place +"&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + api_key # noqa
    #
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    location = None
    #
    if "candidates" in json_response and len(json_response["candidates"]) > 0:
        candidates = json_response["candidates"][0]
        if "geometry" in candidates:
            location = json_response["candidates"][0]["geometry"]["location"]
    #
    return location


def geolocate_place_from_user(api_key: str, business_name: str, lat: float, lng: float, limit: int = 5000) -> Any: # noqa
    locations = []
    radius = 1500
    radius_step = 1500
    while True:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(lat) +"%2C"+ str(lng) +"&radius="+ str(radius) +"&keyword="+ business_name +"&key="+ api_key # noqa
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = json.loads(response.text)
        # if the limit is reached
        if radius - radius_step >= limit:
            break
        # if the response status is not OK #  "status" : "ZERO_RESULTS"
        if json_response["status"] != "OK":
            radius += radius_step
        #
        else:
            results = json_response["results"]
            for result in results:
                locations.append("- " + result["name"])
            if len(locations) > 0:
                break
    return locations


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
        global IS_OP_SELECT, IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE
        self.type_ = json_["type"] if "type" in json_ else ""
        self.op_ = json_["op"] if "op" in json_ else ""
        self.column_ = json_["column"] if "column" in json_ else ""
        self.next_op = json_["next_op"] if "next_op" in json_ else ""
        #
        msg_1 = "is an unknown operation. Notify the system administrator"
        msg_2 = '''is an unknow operation type. Please notify the system
        administrator'''
        if (self.type_ is not None
                and self.type_ in OP_TYPE_LIST
                and self.op_ is not None):
            #
            if self.type_ == OP_TYPE_OUT:
                if (self.op_.startswith(OP_SELECT) and self.column_ is not None): # noqa
                    IS_OP_SELECT = True
                elif self.op_ == OP_CALENDAR_LIST_DAYS_2_RESERVE:
                    IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = True
                else:
                    IS_OP_SELECT = False
                    IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
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
            return_ = self.run_out(json_)
        elif self.type_ == OP_TYPE_SAVE:
            return_ = self.run_save(json_)
        #
        return return_

    def is_empty(self, json_: Any) -> bool:
        return "op" not in json_

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
        #
        return return_

    def run_out(self, json_: Any, list_available_answers: Any) -> Any:
        global IS_OP_SELECT, IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE
        self.parse(json_)
        operation = json_["op"]
        return_proposal = {}
        return_array = []
        is_cldtr = False
        # if operation select in DB
        if IS_OP_SELECT:
            result_ = DB().select(operation)
            i = 0
            for r in result_:
                return_array.append(list_available_answers[i] + ". " + r[json_["column"]]) # noqa
                return_proposal[list_available_answers[i]] = r[json_["column"]]
                i += 1
        elif IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE:
            is_cldtr = IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE
            IS_OP_CALENDAR_LIST_DAYS_TO_RESERVE = False
            tmp_array = get_list_days_to_reserve("1") # noqa
            for i in range(0, len(tmp_array)):
                return_array.append(list_available_answers[i] + ". " + tmp_array[i]) # noqa
                return_proposal[list_available_answers[i]] = tmp_array[i]
        return {
            "is_calendar_list_days_to_reserve": is_cldtr, # noqa
            "proposal": return_proposal,
            "array": return_array
        }

    def run_save(self, json_: Any) -> Any:
        self.parse(json_)
        return {
            "param": json_["param"]
        }

    def run_map(self,
                api_key: str,
                response_msg: str,
                country: str,
                business_name: str
                ) -> Any:
        # self.parse(json_)
        location = geolocate_user(api_key, response_msg, country)
        return geolocate_place_from_user(
            api_key,
            business_name,
            location["lat"],
            location["lng"]
        ) if "lat" in location and "lng" in location else None

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
