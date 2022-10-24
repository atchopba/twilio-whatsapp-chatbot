#!/usr/bin/python

from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    
    LANG_PRINCIPAL_ID = 1
    
    MAX_SIZE_TERM_GEN = 8
    
    DEFAULT_RANG = 99999
    
    MYSQL_HOST = environ.get("MYSQL_HOST")
    MYSQL_USER = environ.get("MYSQL_USER")
    MYSQL_PWD = environ.get("MYSQL_PWD")
    MYSQL_DB = environ.get("MYSQL_DB")
    MYSQL_CHARSET = "utf8mb4" # recommended value or utf8
    
    JAVA_PATH = environ.get("JAVA_PATH") #"C:/dev/java/jdk-11.0.4/bin/java.exe"
    JAVA_OPTS = "-mx1000m" # recommended value
    
    STANDFORD_PATH_FRENCH_TAGGER = basedir + "\\resources\\standford-postagger\\models\\french.tagger"
    STANDFORD_PATH_JAR = basedir + "\\resources\\standford-postagger\\stanford-postagger.jar"
