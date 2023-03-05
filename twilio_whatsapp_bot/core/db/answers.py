#!/usr/bin/python

from twilio_whatsapp_bot.core.db.db import DB
from typing import Any


class Answers(DB):
    
    def __init__(self):
        pass


    def insert_data(self, datas: Any) -> int:
        sql = "INSERT INTO answers (question_1, question_2, question_3, question_4, question_5) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql, (datas[1], datas[2], datas[3], datas[4], datas[5]))
                self.connection.commit()
        except Exception as exception:
            print("Erreur lors de l'execution : ", exception)
        self.deconnect()
