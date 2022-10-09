# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 21:36:24 2022

@author: atchopba
"""
from twilio_whatsapp_bot import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
