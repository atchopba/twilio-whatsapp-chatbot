# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template
# import requests
from twilio.twiml.messaging_response import MessagingResponse
from .core.loan_steps import step_first, step_response


# Blueprint Configuration
main_bp = Blueprint('main_bp', 
                    __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route("/")
def hello():
    return render_template("index.html")
    

@main_bp.route("/bot", methods=["POST"])
def bot():
    # add webhook logic here and return a response
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    
    if "emprunt" in incoming_msg:
        msg.body(step_first())
    
    else:
        msg.body(step_response(incoming_msg))
    
    return str(resp)
