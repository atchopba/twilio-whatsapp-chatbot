#!/usr/bin/python
from twilio_whatsapp_bot import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=True)
