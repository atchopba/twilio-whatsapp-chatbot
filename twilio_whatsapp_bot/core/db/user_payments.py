#!/usr/bin/python
from twilio_whatsapp_bot.core.db.db import DB


class UserPayments(DB):

    def __init__(self):
        pass

    def is_data_exists(self, user_token: str, payment_token: str) -> bool:
        sql = "SELECT * FROM user_payments WHERE is_confirmed <> '1' AND user_token = '{0}' AND payment_token = '{1}'".format(user_token, payment_token) # noqa
        rows = self.select(sql)
        return len(rows) > 0 if rows else -1

    def update_data(self, user_token: str, payment_token: str) -> int:
        sql = "UPDATE user_payments SET is_confirmed = '1' WHERE is_confirmed <> '1' AND user_token = '{0}' AND payment_token = '{1}'".format(user_token, payment_token) # noqa
        return self.insert_without_datas(sql)
