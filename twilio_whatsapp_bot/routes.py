#!/usr/bin/python
from flask import Blueprint, request, render_template
# import requests
from twilio.twiml.messaging_response import MessagingResponse
from .core.api import step_question, step_response

global is_begin_dialog

is_begin_dialog = True
current_step = 0

# Blueprint Configuration
main_bp = Blueprint("main_bp", 
                    __name__,
                    template_folder="templates",
                    static_folder="static")

@main_bp.route("/")
def hello():
    return render_template("index.html")
    

@main_bp.route("/bot", methods=["POST"])
def bot():
    global is_begin_dialog
    ## print("===> request : ", request.values)
    # add webhook logic here and return a response
    incoming_msg = request.values.get("Body", "").lower().strip()
    resp = MessagingResponse()
    msg = resp.message()

    if is_begin_dialog:
        # the initial step is 0
        msg.body(f"{step_question(0)}")
        is_begin_dialog = False
    
    else:
        step_response_ = step_response(incoming_msg)
        msg_tokens = step_response_['tokens']
        msg.body(f"{msg_tokens[0]}")
        is_begin_dialog = step_response_['is_last_dialog']
        #
        msg_list = []
        #
        for i in range (1, len(msg_tokens)):
            msg_list.append(resp.message())
            msg_list[i-1].body(f"{msg_tokens[i]}")

        # add media
        if step_response_["media"] is not None and step_response_["media"] != "":
            msg_media_list = []
            i = 0
            for media_ in step_response_["media"]:
                if media_["url"] is not None and media_["url"] != "":
                    msg_media_list.append(resp.message())
                    msg_media_list[i].media(f"{media_['url']}")
                    i += 1

    return str(resp)
