#!/usr/bin/python
from os import listdir
from os.path import isfile, join
from parse import parse
from pathlib import Path
from typing import Any


def get_data_from_url(received_message: str, index: str) -> str:
    template = 'SmsMessageSid={SmsMessageSid}&NumMedia={NumMedia}&ProfileName={ProfileName}&SmsSid={SmsSid}&WaId={WaId}&SmsStatus={SmsStatus}&Body={Body}&To={To}&NumSegments={NumSegments}&ReferralNumMedia={ReferralNumMedia}&MessageSid={MessageSid}&AccountSid={AccountSid}&From={From}&ApiVersion={ApiVersion}'
    tokens = parse(template, received_message)
    return tokens[index]


def get_list_files(pathdir: str) -> Any:
    onlyfiles = [f for f in listdir(pathdir) if isfile(join(pathdir, f))]
    return onlyfiles


def get_file_content(filepath: str) -> str:
    file_content = ""
    try:
        file_content = Path(filepath).read_text(encoding="UTF-8").strip()
    except Exception as exception:
        print("Error occurs while opening file : ", exception)
    return file_content
