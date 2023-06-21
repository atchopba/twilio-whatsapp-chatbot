#!/usr/bin/python

from typing import Any
import pymysql.cursors
from collections import namedtuple

from config import Config

ResultSelectQuery = namedtuple("ResultSelectQuery", "result error_msg")


class DB(object):

    def __init__(self):
        pass

    def connect(self) -> None:
        '''
        Connect to the database with params define into .env file

        Returns
        -------
        None.

        '''
        try:
            self.connection = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PWD,
                db=Config.MYSQL_DB,
                charset=Config.MYSQL_CHARSET,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(e)

    def deconnect(self) -> None:
        '''
        Deconnect to the database

        Returns
        -------
        None.

        '''
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def select(self, r, select_one: bool = False) -> Any:
        '''
        Select data into a table

        Parameters
        ----------
        r : String
            Request to execute.
        select_one : Boolean, optional
            Specify if select one row data or many. The default is False.

        Returns
        -------
        Array
            Row data.

        '''
        self.connect()
        error_msg = ""
        result = []
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(r)
                result = cursor.fetchall() if (
                    select_one is False) else [cursor.fetchone()]
        except Exception as e:
            error_msg = "Erreur lors de l'execution : ", e
            print(error_msg)
        self.deconnect()
        return result

    def is_result(self, r):
        return len(r) > 0 and r[0] is not None

    def insert(self, sql: str, datas: Any) -> int:
        '''
        Insert a row data into a table

        Parameters
        ----------
        sql : String
            Request to execute.
        datas : Any
            Row data to insert

        Returns
        -------
        Int
            Number of rows data inserts.

        '''
        self.connect()
        return_ = -1
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, datas)
                self.connection.commit()
                return_ = cursor.rowcount
        except Exception as exception:
            print("Erreur lors de l'execution : ", exception)
        self.deconnect()
        return return_
