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
import datetime
from twilio_whatsapp_bot.core.utilies.cal_setup import get_calendar_service


DEFAULT_CALLING_CODE = Config.DEFAULT_CALLING_CODE
WORK_ON_SATURDAY = True if Config.WORK_ON_SATURDAY.lower() == "true" else False # noqa
WORK_ON_SUNDAY = True if Config.WORK_ON_SUNDAY.lower() == "true" else False # noqa


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


def replace_assistant_in_content(file_content: str, assistant: str) -> str:
    return file_content.replace("{ASSISTANT}", assistant).replace("{assistant}", assistant) # noqa


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
    return ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"] if is_response_alpha else ["1","2","3","4","5","6","7","8","9","10","11","12"] # noqa


def get_list_days_to_reserve(lang: str) -> Any:
    days = {
        "monday": "Lundi",
        "tuesday": "Mardi",
        "wednesday": "Mercredi",
        "thursday": "Jeudi",
        "friday": "Vendredi",
        "saturday": "Samedi",
        "sunday": "Dimanche"
    }
    i = 0
    array_ = []
    while len(array_) < 6:
        date_tmp = datetime.datetime.now() + datetime.timedelta(days=i)
        dayofweek = date_tmp.strftime('%A')
        if lang != "2":
            dayofweek = days[date_tmp.strftime('%A').lower()]
        # if not (5 <= date_tmp.weekday() <= 6):
        weekday = date_tmp.weekday()
        if ((WORK_ON_SATURDAY and weekday == 5) or
            (WORK_ON_SUNDAY and weekday == 6) or (weekday != 5 and weekday != 6)) :  # noqa
            # print("==> ", (str(dayofweek) + " " + str(date_tmp.strftime("%d/%m/%Y"))))  # noqa
            array_.append(str(dayofweek) + " " + str(date_tmp.strftime("%d/%m/%Y")))  # noqa
        i = i+1
    return array_


def calendar_create_event(timeZone: str, summary: str, description: str,
                          day_: str, start: str, end: str,
                          color: str) -> Any:
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()
    #
    tmp_day = day_.split("/")
    tomorrow = datetime.datetime(
        int(tmp_day[2]),
        int(tmp_day[1]),
        int(tmp_day[0])
    )
    start_tmp = start.split(":")
    end_tmp = end.split(":")
    start = (tomorrow + datetime.timedelta(hours=int(start_tmp[0]), minutes=int(start_tmp[1]))).isoformat()  # noqa
    end = (tomorrow + datetime.timedelta(hours=int(end_tmp[0]), minutes=int(end_tmp[1]))).isoformat()  # noqa
    #
    event_result = service.events().insert(calendarId='primary',
        body = { # noqa
            "summary": summary,
            "description": description,
            "colorId": color,
            "start": {"dateTime": start, "timeZone": timeZone},
            "end": {"dateTime": end, "timeZone": timeZone},
        }
    ).execute()
    #
    return event_result["id"] if event_result["id"] is not None else ""
