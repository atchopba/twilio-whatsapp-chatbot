#!/usr/bin/python
import json
from typing import Any
import re


PATTERN_DATA = r"^\{\"data\"\:\s*\"[a-z*\s'=_]*\"(,\s*\"[a-z*\s_]*\"\:\s*\"[a-zA-Z0-9*\s'=_\/\:\.,-]*\")+\}$" # noqa

TYPE_IMG_GIF = "image/gif"
TYPE_IMG_JPEG = "image/jpeg"
TYPE_IMG_PNG = "image/png"

LIST_TYPE_IMG = {TYPE_IMG_GIF, TYPE_IMG_JPEG, TYPE_IMG_PNG}


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
        'datas_found': datas_found,  # json.dumps(datas_found),
        'msg': clean_data_from_question_content(bot_dialog)
    }


def parse(json_) -> None:
    data_ = json_["data"] if "data" in json_ else ""
    type_ = json_["type"] if "type" in json_ else ""
    url_ = json_["url"] if "url" in json_ else ""
    #
    msg_1 = "is an unknown data. Notify the system administrator"
    msg_2 = "is an unknown type data. Notify the system administrator"
    msg_3 = "is an unknown url data. Notify the system administrator"
    #
    if data_ is not None and data_ != "data":
        pass
    else:
        raise Exception("{%s} " + msg_1, data_)
    #
    if (type_ is not None
            and type_ not in LIST_TYPE_IMG):
        pass
    else:
        raise Exception("{%s} " + msg_2, type_)
    #
    if url_ is not None and type_ != "":
        pass
    else:
        raise Exception("{%s} " + msg_3, url_)
    #
    return True
