#!/usr/bin/python

from twilio_whatsapp_bot.core.db.db import DB
from typing import Any


class UserActivities(DB):

    def __init__(self):
        # super().__init__()
        self.table_ = 'user_activities'

    def insert_data(self, user_token: str, action_param: str, action_value_1: str) -> bool: # noqa
        sql = """INSERT INTO {0} (user_token, action_param, action_value_1) 
        VALUES ('{1}', '{2}', '{3}')""".format(
            self.table_, user_token, action_param, action_value_1
        )
        return self.insert_without_datas(sql)

    def get_by_user_token(self, user_token: str) -> Any:
        r = "SELECT * FROM {0} WHERE user_token='{1}'".format(self.table_, user_token) # noqa
        cursor = self.execute_query(r)
        return [row['action_value_1'] for row in cursor.result] # noqa
