#!/usr/bin/python
import json
import re
from twilio_whatsapp_bot.core.db.db import DB
from twilio_whatsapp_bot.core.helpers import check_noun, check_number, check_phonenumber, check_str, chech_email
from typing import Any


OP_TYPE_OUT = "out"
OP_TYPE_IN = "in"

OP_CHECK_NOUN = "check_noun"
OP_CHECK_STR = "check_str"
OP_CHECK_NUMBER = "check_number"
OP_CHECK_PHONENUMBER = "check_phonenumber"
OP_CHECK_CITY = "check_city"
OP_CHECK_EMAIL = "check_email"
OP_SELECT = "select"

OP_LIST = {OP_CHECK_CITY, OP_CHECK_NOUN, OP_CHECK_NUMBER, OP_CHECK_PHONENUMBER, OP_CHECK_STR, OP_CHECK_EMAIL}


#PATTERN_OPERATION = r"^\[[a-zA-Z]{3,10}\_[a-zA-Z]{3,20}\]$"
#PATTERN_OPERATION = r"^\{\"[a-z*\s_]*\"\:\s*\"[a-z*\s'=_]*\"(,\s*\"[a-z*\s_]*\"\:\s*\"[a-z*\s'=_]*\")+\}$"
PATTERN_OPERATION = r"^\{\"type\"\:\s*\"[a-z*\s'=_]*\"(,\s*\"[a-zA-Z*\s_]*\"\:\s*\"[a-zA-Z*\s'=_(),-;]*\")+\}$"


def clean_operations_from_question_content(msg: str) -> str:
    tmp_ = re.sub(PATTERN_OPERATION, "", msg, 0, re.MULTILINE)
    if tmp_ != msg:
        tmp_ = tmp_.replace("\n", "")
    return tmp_
    

def get_operations_in_bot_dialog(bot_dialog: str) -> Any:
    operations_found = ""
    bot_dialog = bot_dialog.lower()
    for match in re.finditer(PATTERN_OPERATION, bot_dialog, re.MULTILINE):
        operations_found = match.group()
        break
    return {
        'operations_found': json.loads(operations_found) if operations_found != "" else "",
        'msg': clean_operations_from_question_content(bot_dialog)
    }


class Operation(object):
    
    def __init__(self):
        self.type_ = ""
        self.op_ = ""
        self.column_ = ""
        pass


    '''
    Parse the json define in json
    @raise Exception 
    '''
    def parse(self, json_) -> None:
        self.type_ = json_["type"] if "type" in json_ else ""
        self.op_ = json_["op"] if "op" in json_ else ""
        self.column_ = json_["column"] if "column" in json_ else ""
        #
        if self.type_ is not None and self.type_ in (OP_TYPE_IN, OP_TYPE_OUT) and self.op_ is not None:
            #   
            if self.type_ == OP_TYPE_OUT and self.op_.startswith(OP_SELECT) and self.column_ is not None:
                pass
            #
            elif self.type_ == OP_TYPE_IN and self.op_ in OP_LIST:
                pass
            #
            else:
                raise Exception("{} is an unknown operation. Notify the system administrator", self.op_)
        # 
        else:
            raise Exception("{} is an unknow operation type. Please notify the system administrator", self.type_)
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
        #
        return return_


    def is_empty(self, json_: Any) -> bool:
        return not "op" in json_


    def is_run_in(self, json_: Any) -> bool:
        return not self.is_empty(json_) and json_["type"] == OP_TYPE_IN


    def is_run_out(self, json_: Any) -> bool:
        return not self.is_empty(json_) and json_["type"] == OP_TYPE_OUT
    
    
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
            return_ = chech_email(msg_2_check)
        #
        return return_
    

    def run_out(self, json_: Any) -> Any:
        self.parse(json_)
        result_ = DB().select(json_["op"])
        return_ = []
        i = 1
        for r in result_:
            return_.append(str(i) + ". "+ r[json_["column"]])
            i += 1
        return return_
    