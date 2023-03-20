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
        msg.body(f"{step_response_['quote']}")
        is_begin_dialog = step_response_['is_last_dialog']
    
    return str(resp)
