#!/usr/bin/python
from parse import parse
from pathlib import Path
from typing import Any
import glob
import json


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
            #print("list_A mot : ", key)
            #print("list_B mot : ",word)
            res += 1 if key in sentence else 0
        if res_index < res:
            res_index = res
            index = i
        return_.append(res)
        
    return index


def count_word(sentence: str, word: str) -> int:
    import re
    a = re.split(r'\W', sentence)
    return a.count(word)
