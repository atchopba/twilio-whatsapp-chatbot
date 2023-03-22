#!/usr/bin/python

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    
    MYSQL_HOST = environ.get("MYSQL_HOST")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PWD = environ.get("MYSQL_PWD")
    MYSQL_DB = environ.get("MYSQL_DB")
    MYSQL_CHARSET = "utf8mb4" # recommended value or utf8

    BAD_ANSWER_STR = environ.get("BAD_ANSWER_STR")
    BAD_ANSWER_CHOICE_STR = environ.get("BAD_ANSWER_CHOICE_STR")
