#!/usr/bin/python

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:

    IS_SAVE_IN_DB = environ.get("IS_SAVE_IN_DB")
    MYSQL_HOST = environ.get("MYSQL_HOST")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PWD = environ.get("MYSQL_PWD")
    MYSQL_DB = environ.get("MYSQL_DB")
    MYSQL_CHARSET = "utf8mb4"  # recommended value or utf8

    PATH_TO_DIALOG = environ.get("PATH_TO_DIALOG")

    BAD_ANSWER_STR = environ.get("BAD_ANSWER_STR")
    BAD_ANSWER_CHOICE_STR = environ.get("BAD_ANSWER_CHOICE_STR")

    PROPOSE_ALL_QUESTIONS_FOLDER_STR = environ.get("PROPOSE_ALL_QUESTIONS_FOLDER_STR") # noqa

    DEFAULT_CALLING_CODE = environ.get("DEFAULT_CALLING_CODE")

    DIALOG_ASSISTANT = environ.get("DIALOG_ASSISTANT")

    GOOGLE_MAPS_API_KEY = environ.get("GOOGLE_MAPS_API_KEY")

    DEFAULT_MAPS_LOCATION_ERROR = environ.get("DEFAULT_MAPS_LOCATION_ERROR")

    BUSINESS_NAME = environ.get("BUSINESS_NAME")

    DEFAULT_COUNTRY = environ.get("DEFAULT_COUNTRY")

    DEFAULT_MOMO_URL = environ.get("DEFAULT_MOMO_URL")

    DEFAULT_PAYMENT_VALIDATED_STR = environ.get("DEFAULT_PAYMENT_VALIDATED_STR")

    WORK_ON_SATURDAY = environ.get("WORK_ON_SATURDAY")

    WORK_ON_SUNDAY = environ.get("WORK_ON_SUNDAY")

    BUSINESS_GEOLOCATE_SENTENCE = environ.get("BUSINESS_GEOLOCATE_SENTENCE")

    IS_RESPONSE_ALPHA = environ.get("IS_RESPONSE_ALPHA")
