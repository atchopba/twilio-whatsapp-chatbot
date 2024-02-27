#!/usr/bin/python
from config import Config
from deep_translator import GoogleTranslator
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
    template = ('SmsMessageSid={SmsMessageSid}&NumMedia={NumMedia}' +
                '&ProfileName={ProfileName}&SmsSid={SmsSid}' +
                '&WaId={WaId}&SmsStatus={SmsStatus}&Body={Body}' +
                '&To={To}&NumSegments={NumSegments}' +
                '&ReferralNumMedia={ReferralNumMedia}' +
                '&MessageSid={MessageSid}&AccountSid={AccountSid}' +
                '&From={From}&ApiVersion={ApiVersion}')
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


def replace_words_in_content(file_content: str, regex_: str, words: str) -> str: # noqa
    regex_lower = regex_.lower()
    regex_upper = regex_.upper()
    return_ = file_content.replace(regex_lower, words)
    return return_.replace(regex_upper, words)


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
    return True if (
        not re.findall(r"[a-zA-Z0-9]\.\s*", content, re.MULTILINE | re.DOTALL)
    ) else False


def count_nb_folders(input_path: str = "./data/dialog/questions/") -> int:
    folder_count = 0  # type: int
    if not check_folder_exists(input_path):
        return -1
    for folders in os.listdir(input_path):  # loop over all files
        # if it's a directory
        if os.path.isdir(os.path.join(input_path, folders)):
            folder_count += 1
    return folder_count


def change_filepath(filepath: str) -> str:
    return filepath.replace("\\", "/").replace("/", "_").replace(".", "_")


def check_number(msg_2_check: str) -> bool:
    return msg_2_check is not None and msg_2_check.isnumeric()


def check_str(msg_2_check: str) -> bool:
    return (isinstance(msg_2_check, str) and
            any(ele in msg_2_check for ele in ["a", "e", "i", "o", "u", "y"]))


def check_noun(msg_2_check: str) -> bool:
    return check_str(msg_2_check)


def check_phonenumber(msg_2_check: str) -> bool:
    msg_2_check = msg_2_check.replace("%2b", "+")
    if not msg_2_check.startswith("+"):
        msg_2_check = DEFAULT_CALLING_CODE + msg_2_check
    pattern = re.compile(r"^(\+){0,1}\d{8,12}$")
    return bool(pattern.match(msg_2_check))


def check_email(email_adr: str) -> bool:
    email_adr = email_adr.replace("%40", "@")
    return True if re.match(r"[^@]+@[^@]+\.[^@]+", email_adr) else False


def random_generator() -> str:
    import string
    import secrets
    alphabet = string.ascii_letters + string.digits + "-_+$()#@"
    password = ''.join(secrets.choice(alphabet) for i in range(32))
    return password


def translate_msg(tokens: Any, from_lang: str, to_lang: str) -> Any:
    if from_lang != to_lang:
        tmp_tokens = []
        for token in tokens:
            if token != "" and token.strip() != "":
                translator = GoogleTranslator(source='auto', target=to_lang)
                tmp_tokens.append(translator.translate(token))
        return tmp_tokens
    return tokens


def available_answers(bot_dialog: str, trash: str = ".") -> Any:
    REGEX_PATTERN = r"^[\d|\w|\W]\. "
    return_ = []
    for match in re.finditer(REGEX_PATTERN, bot_dialog, re.MULTILINE):
        tmp = match.group().strip().replace(trash, "")
        return_.append(tmp.lower())
        if (tmp.lower() != tmp.upper()):
            return_.append(tmp.upper())
    return return_


def get_list_available_answer_run_out(is_response_alpha: bool = False) -> Any:
    return ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"] if is_response_alpha else ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26"] # noqa


def is_part(root: str, search: str):
    return True if re.search(search, root, re.IGNORECASE) else False


def get_payment_token(root: str) -> str:
    tmp_ = root.split(':')
    return tmp_[len(tmp_) - 1].strip()
