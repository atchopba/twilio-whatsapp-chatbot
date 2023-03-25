#!/usr/bin/python
import glob
import json
from parse import parse
from pathlib import Path
import re
from typing import Any


#PATTERN_OPERATION = r"^\[[a-zA-Z]{3,10}\_[a-zA-Z]{3,20}\]$"
PATTERN_OPERATION = r"^\{\"[a-z*\s_]*\"\:\s*\"[a-z*\s'=_]*\"(,\s*\"[a-z*\s_]*\"\:\s*\"[a-z*\s'=_]*\")+\}$"


def get_data_from_url(received_message: str, index: str) -> str:
    template = 'SmsMessageSid={SmsMessageSid}&NumMedia={NumMedia}&ProfileName={ProfileName}&SmsSid={SmsSid}&WaId={WaId}&SmsStatus={SmsStatus}&Body={Body}&To={To}&NumSegments={NumSegments}&ReferralNumMedia={ReferralNumMedia}&MessageSid={MessageSid}&AccountSid={AccountSid}&From={From}&ApiVersion={ApiVersion}'
    tokens = parse(template, received_message)
    return tokens[index]


def get_list_files(pathdir: str) -> Any:
    files = glob.glob(pathdir + '/**/*.txt', recursive=True)
    return files


def get_file_content(filepath: str) -> str:
    file_content = ""
    try:
        file_content = Path(filepath).read_text(encoding="UTF-8").strip()
    except Exception as exception:
        print("Error occurs while opening file : ", exception)
    return file_content


def load_json_file(file_path: str = "./data/dialog/questions/0.json") -> Any:
    return json.load(open(file_path))


def check_probability_and_return_folder(sentence: str, data_array: Any, column_array: str = "words") -> Any:
    return_ = []
    index = 0
    res_index = 0
    
    for i in range(0, len(data_array)):
        data_ = data_array[i]
        list_A = data_[column_array].split("-")
        res = 0
        for key in list_A:
            res += 1 if key in sentence else 0
        if res_index < res:
            res_index = res
            index = i
        return_.append(res)
        
    return index


def count_word(sentence: str, word: str) -> int:
    a = re.split(r'\W', sentence)
    return a.count(word)


def clean_question_content(msg: str) -> str:
    tmp_ = re.sub(PATTERN_OPERATION, "", msg, 0, re.MULTILINE)
    if tmp_ != msg:
        tmp_ = tmp_.replace("\n", "")
    return tmp_


def get_operations_in_bot_dialog(bot_dialog: str) -> Any:
    operations_found = ""
    for match in re.finditer(PATTERN_OPERATION, bot_dialog, re.MULTILINE):
        operations_found = match.group()
        break
    return {
        'operations_found': json.loads(operations_found) if operations_found != "" else "",
        'msg': clean_question_content(bot_dialog)
    }


def check_number(msg_2_check: str) -> bool:
    return msg_2_check is not None and msg_2_check.isnumeric()


def check_str(msg_2_check: str) -> bool:
    return isinstance(msg_2_check, str) and any(ele in msg_2_check for ele in ["a", "e", "i", "o", "u", "y"])


def check_noun(msg_2_check: str) -> bool:
    return check_str(msg_2_check)


def check_phonenumber(msg_2_check: str) -> bool:
    import phonenumbers
    from phonenumbers import carrier
    from phonenumbers.phonenumberutil import number_type
    #
    if not msg_2_check.startswith("+"):
        msg_2_check = "+237" + msg_2_check
    #
    return carrier._is_mobile(number_type(phonenumbers.parse(msg_2_check)))
