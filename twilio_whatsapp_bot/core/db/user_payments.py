#!/usr/bin/python
from twilio_whatsapp_bot.core.db.db import DB


class UserPayments(DB):

    def __init__(self):
        pass

    def select_data(self, user_token: str, payment_token: str) -> bool:
        sql = "SELECT * FROM user_payments WHERE is_confirmed <> '1' AND user_token = '{0}' AND payment_token = '{1}'".format(user_token, payment_token) # noqa
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()
                return len(rows) > 0
        except Exception as exception:
            print("Erreur lors de l'execution : ", exception)
        self.deconnect()
        return False

    def update_data(self, user_token: str, payment_token: str) -> int:
        sql = "UPDATE user_payments SET is_confirmed = '1' WHERE is_confirmed <> '1' AND user_token = '{0}' AND payment_token = '{1}'".format(user_token, payment_token) # noqa
        try:
            self.connect()
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as exception:
            print("Erreur lors de l'execution : ", exception)
        self.deconnect()
