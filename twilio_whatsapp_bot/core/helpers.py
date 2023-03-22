#!/usr/bin/python
import glob
import json
from parse import parse
from pathlib import Path
import re
from typing import Any


PATTERN_OPERATION = r"^\[[a-zA-Z]{3,10}\_[a-zA-Z]{3,20}\]$"

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
    return re.sub(PATTERN_OPERATION, "", msg, 0, re.MULTILINE)


def get_operations_in_bot_dialog(bot_dialog: str) -> Any:
    pattern = PATTERN_OPERATION
    operations_found = []
    tmp_bot_dialog = bot_dialog
    for op in re.findall(pattern, bot_dialog, re.MULTILINE):
        operations_found.append(op)
        tmp_bot_dialog = tmp_bot_dialog.replace(op, "")
    return {
        'operations_found': operations_found,
        'msg': tmp_bot_dialog.replace("\n", "")
    }
