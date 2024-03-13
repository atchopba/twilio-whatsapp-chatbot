#!/usr/bin/python
from config import Config
import json
import qrcode
import re
import requests
import datetime
from twilio_whatsapp_bot.core.db.db import DB
from twilio_whatsapp_bot.core.db.user_activities import UserActivities
from twilio_whatsapp_bot.core.db.user_payments import UserPayments
from twilio_whatsapp_bot.core.helpers import random_generator
from typing import Any


# PATTERN_OPERATION = r"^\{\"type\"\:\s*\"[a-z0-9*\s'=_]*\"(,\s*\"[a-zA-Z*\s_]*\"\:\s*\"[a-zA-Z*\s'=_(),-;]*\")+\}$"  # noqa
# PATTERN_OPERATION =  r"^\{\"type\"\:\s*\".*?\"(,\s*\".*?\"\:\s*\".*?\")+\}$"
PATTERN_OPERATION = r"^\{\"type\"\:\s*\".*?\"(,\s*\".*?\"\:\s*((\".*?\")|(\{\".*?\"\:\s*\".*?\"(,\s*\".*?\"\:\s*\".*?\")+\})))+\}$" # noqa

WORK_ON_SATURDAY = True if Config.WORK_ON_SATURDAY.lower() == "true" else False # noqa
WORK_ON_SUNDAY = True if Config.WORK_ON_SUNDAY.lower() == "true" else False # noqa

PATH_QRCODE = Config.PATH_QRCODE
URL_QRCODE = Config.URL_QRCODE


def clean_operations_from_question_content(msg: str) -> str:
    tmp_ = re.sub(PATTERN_OPERATION, "", msg, 0, re.MULTILINE)
    return tmp_


def get_operations_in_bot_dialog(bot_dialog: str) -> Any:
    operations_found = []
    tmp_bot_dialog = bot_dialog.lower()
    for match in re.finditer(PATTERN_OPERATION, tmp_bot_dialog, re.MULTILINE):
        operations_found.append(json.loads(match.group()))
    return {
        'operations_found': operations_found,
        'msg': clean_operations_from_question_content(bot_dialog)
    }


def geolocate_user(api_key: str, search_place: str, country: str) -> Any:
    search_place = search_place.replace("  ", " ")
    search_place += ", " + country
    search_place = search_place.replace(" ", "%20")
    url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="+ search_place +"&inputtype=textquery&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key=" + api_key # noqa
    #
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    location = None
    #
    if "candidates" in json_response and len(json_response["candidates"]) > 0:
        candidates = json_response["candidates"][0]
        if "geometry" in candidates:
            location = json_response["candidates"][0]["geometry"]["location"]
    #
    return location


def geolocate_place_from_user(api_key: str, business_name: str, lat: float, lng: float, limit: int = 5000) -> Any: # noqa
    locations = []
    radius = 1500
    radius_step = 1500
    while True:
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+ str(lat) +"%2C"+ str(lng) +"&radius="+ str(radius) +"&keyword="+ business_name +"&key="+ api_key # noqa
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        json_response = json.loads(response.text)
        # if the limit is reached
        if radius - radius_step >= limit:
            break
        # if the response status is not OK #  "status" : "ZERO_RESULTS"
        if json_response["status"] != "OK":
            radius += radius_step
        #
        else:
            results = json_response["results"]
            for result in results:
                locations.append("- " + result["name"])
            if len(locations) > 0:
                break
    return locations


def get_list_days_to_reserve(lang: str) -> Any:
    days = {
        "monday": "Lundi",
        "tuesday": "Mardi",
        "wednesday": "Mercredi",
        "thursday": "Jeudi",
        "friday": "Vendredi",
        "saturday": "Samedi",
        "sunday": "Dimanche"
    }
    i = 0
    array_ = []
    while len(array_) < 6:
        date_tmp = datetime.datetime.now() + datetime.timedelta(days=i)
        dayofweek = date_tmp.strftime('%A')
        if lang != "2":
            dayofweek = days[date_tmp.strftime('%A').lower()]
        # if not (5 <= date_tmp.weekday() <= 6):
        weekday = date_tmp.weekday()
        if ((WORK_ON_SATURDAY and weekday == 5) or
            (WORK_ON_SUNDAY and weekday == 6) or (weekday != 5 and weekday != 6)) :  # noqa
            array_.append(str(dayofweek) + " " + str(date_tmp.strftime("%d/%m/%Y")))  # noqa
        i = i+1
    return array_


def make_new_token() -> str:
    token_lst = DB().select("select user_token from user_sessions")
    term_ = random_generator()
    while term_ in token_lst:
        term_ = random_generator()
    # insert into user_sessions
    sql = "INSERT INTO user_sessions (user_token) VALUES ('{0}')".format(term_)
    DB().insert_without_datas(sql)
    #
    return term_


def update_payment_data(user_token, payment_token):
    if UserPayments().select_data(user_token, payment_token):
        UserPayments().update_data(user_token, payment_token)
        UserActivities().insert_data(user_token, 'update_payment with payment_token: ' + payment_token, 'payment validated') # noqa
        return {
            'status': 'OK',
            'message': 'La transaction a été  mise à jour'
        }
    return {
        'status': 'NOK',
        'message': 'Le jeton nous semble erroné'
    }


def get_operations_by_type(array_operations: Any, type_: str) -> Any:
    for operation in array_operations:
        if 'type' in operation and operation['type'] == type_:
            return operation
    return None


def generate_token(user_token):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # select data in user_activities
    user_activities_data = UserActivities().get_by_user_token(user_token)
    # and add data in the QR-code
    for activity in user_activities_data:
        qr.add_data(activity + '\n')
    # generate and save image on a web server
    img = qr.make_image(fill_color='black', back_color='white')
    qrcode_path = PATH_QRCODE + '/' + str(user_token) + '.png'
    img.save(qrcode_path)
    # save in user_activities
    UserActivities().insert_data(user_token, 'QRCODE generated', qrcode_path)
    # return the url
    return URL_QRCODE + '/' + str(user_token) + '.png'
