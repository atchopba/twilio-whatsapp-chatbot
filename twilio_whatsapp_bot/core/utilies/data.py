#!/usr/bin/python
import json
from typing import Any
import re


PATTERN_DATA = r"^\{\"data\"\:\s*\"[a-z*\s'=_]*\"(,\s*\"[a-z*\s_]*\"\:\s*\"[a-zA-Z0-9*\s'=_\/\:\.,-]*\")+\}$"

TYPE_IMG_GIF = "image/gif"
TYPE_IMG_JPEG = "image/jpeg"
TYPE_IMG_PNG = "image/png"


def clean_data_from_question_content(msg: str) -> str:
    tmp_ = re.sub(PATTERN_DATA, "", msg, 0, re.MULTILINE)
    if tmp_ != msg:
        tmp_ = tmp_.replace("\n", "")
    return tmp_


def get_datas_in_bot_dialog(bot_dialog: str) -> Any:
    datas_found = []
    for match in re.finditer(PATTERN_DATA, bot_dialog, re.MULTILINE):
        datas_found.append(json.loads(match.group(0)))
    #
    return {
        'datas_found': datas_found, #json.dumps(datas_found),
        'msg': clean_data_from_question_content(bot_dialog)
    }


class Data(object):
    
    def __init__(self):
        self.data_ = ""
        self.type_ = ""
        self.url_ = ""
    

    '''
    Parse the json define in json
    @raise Exception 
    '''
    def parse(self, json_) -> None:
        self.data_ = json_["data"] if "data" in json_ else ""
        self.type_ = json_["type"] if "type" in json_ else ""
        self.url_ = json_["url"] if "url" in json_ else ""
        #
        if self.data_ is not None and self.data_ != "data":
            pass
        else:
            raise Exception("{%s} is an unknown data. Notify the system administrator", self.data_)
        #
        if self.type_ is not None and self.type_ not in (TYPE_IMG_GIF, TYPE_IMG_JPEG, TYPE_IMG_PNG):
            pass
        else:
            raise Exception("{%s} is an unknown type data. Notify the system administrator", self.type_)
        # 
        if self.url_ is not None and self.type_ != "":
            pass
        else:
            raise Exception("{%s} is an unknown url data. Notify the system administrator", self.url_)
        #
        return True
        