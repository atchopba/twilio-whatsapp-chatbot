#!/usr/bin/python
from config import Config
import glob
import json
import os
from parse import parse
from pathlib import Path
import re
from typing import Any
from unidecode import unidecode


DEFAULT_CALLING_CODE = Config.DEFAULT_CALLING_CODE

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


def remove_accents(msg: str) -> str:
    return unidecode(msg)


def replace_assistant_in_content(file_content: str, assistant: str) -> str:
    return file_content.replace("{ASSISTANT}", assistant)


def check_content_is_2_msg(file_content: str) -> Any:
    tokens_ = file_content.split("|")
    #
    for i in range(0, len(tokens_)):
        if tokens_[i].strip() != "":
            tokens_[i] = tokens_[i].strip()
    return {
        "is_in_2_msg": len(tokens_) > 1,
        "tokens": tokens_
    }


def check_folder_exists(path_: str) -> bool:
    return os.path.exists(path_) and len(os.listdir(path_)) > 1


def load_json_file(file_path: str = "./data/dialog/questions/0.json") -> Any:
    return json.load(open(file_path))


def count_word(sentence: str, word: str) -> int:
    a = re.split(r'\W', sentence)
    return a.count(word)


def is_question_without_choice(content: str) -> bool:
    return True if re.findall(r"[a-zA-Z0-9]\.\s*", content, re.MULTILINE|re.DOTALL) else False 


def count_nb_folders(path_: str = "./data/dialog/questions/") -> int:
    return len(next(os.walk(path_))[1])


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
        msg_2_check = DEFAULT_CALLING_CODE + msg_2_check
    #
    try:
        return_ = carrier._is_mobile(number_type(phonenumbers.parse(msg_2_check)))
    except:
        return_ = False
    return return_


def chech_email(email_adr: str) -> bool:
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", email_adr) else False
