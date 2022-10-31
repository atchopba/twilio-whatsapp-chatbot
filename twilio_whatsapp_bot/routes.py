#!/usr/bin/python
from flask import Blueprint, request, render_template
# import requests
from twilio.twiml.messaging_response import MessagingResponse
from .core.api import step_question, step_response, PATHDIR_QUESTIONS
from .core.helpers import get_file_content


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
    ## print("===> request : ", request.values)
    # add webhook logic here and return a response
    incoming_msg = request.values.get("Body", "").lower().strip()
    resp = MessagingResponse()
    msg = resp.message()
    
    if get_file_content(PATHDIR_QUESTIONS + "/0.txt") in incoming_msg:
        msg.body(f"{step_question(1)}")
    
    else:
        msg.body(f"{step_response(incoming_msg)}")
    
    return str(resp)
