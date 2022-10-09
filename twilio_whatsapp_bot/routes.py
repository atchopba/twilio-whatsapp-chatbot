# -*- coding: utf-8 -*-
from flask import Blueprint, request, render_template
import requests
from twilio.twiml.messaging_response import MessagingResponse
#from flask import Blueprint, request, make_response
#from flask import render_template


# Blueprint Configuration
main_bp = Blueprint('main_bp', 
                    __name__,
                    template_folder='templates',
                    static_folder='static')

@main_bp.route("/")
def hello():
    return render_template('index.html')
    

@main_bp.route('/bot', methods=['POST'])
def bot():
    # add webhook logic here and return a response
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    return str(resp)
