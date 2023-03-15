#!/usr/bin/python

from twilio_whatsapp_bot.core.db.db import DB
from typing import Any


class Answers(DB):
    
    def __init__(self):
        pass


    def insert_data(self, datas: Any) -> int:
        insert_params = []
        insert_values = []
        for i in range(0, len(datas)):
            insert_params.append("question_" + str(i))
            insert_values.append("'" + datas[i] + "'")

        sql = "INSERT INTO answers ("+ ",".join(insert_params) +") VALUES ("+ ",".join(insert_values) +")"

        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as exception:
            print("Erreur lors de l'execution : ", exception)
        self.deconnect()
