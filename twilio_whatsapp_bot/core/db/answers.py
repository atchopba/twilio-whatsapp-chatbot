#!/usr/bin/python

from twilio_whatsapp_bot.core.db.db import DB
from typing import Any


class Answers(DB):
    
    def __init__(self):
        pass


    def insert_data(self, datas: Any) -> int:
        sql = "INSERT INTO answers (question_1, question_2, question_3, question_4, question_5, question_6) VALUES (%s, %s, %s, %s, %s, %s)"
        self.insert(sql, datas)
