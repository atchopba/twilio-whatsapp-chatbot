[![Pylint](https://github.com/atchopba/twilio-whatsapp-chatbot/actions/workflows/pylint.yml/badge.svg)](https://github.com/atchopba/twilio-whatsapp-chatbot/actions/workflows/pylint.yml)

# Twilio-whatsapp-chatbot
Twilio whatsapp chatbot.
The dialog is configured in text files. The files are thus read in alphabetical order during the discussion.

## Install

### Python 3.10

- https://www.python.org/downloads/release/python-3109/
- put the folder python310 and python/Scripts in the ennvironment variables


### Ngrok

- https://ngrok.com/download
- connect to the ngrok site and copy the AuthToken https://dashboard.ngrok.com/get-started/your-authtoken


### The code:

- download the code
- install dependencies

```
pip3 install virtualenv
python3 -m venv .venv
source .venv/bin/activate # for Linux 
# .venv/Scripts/activate.bat for Windows
pip3 install -r requirements.txt
```


### MySQL

- the database script creation is into data folder


## Getting started: 

- Rename "init.env" to ".env"
- Edit ".env" file and put the right values

### launching python code

```
python wsgi.py
```

### Launching ngrok

```
ngrok http 4000
```

- Copy the https:// URL from the ngrok output and then paste it on the "When a message comes in" field.
- Add /bot after the url to expose the endpoint

### Twilio

- Go to [Twilio](https://console.twilio.com/) -> Messaging -> send WhatsApp message -> sandbox parameter
- Put your ngrok address here + /bot
![Page index](data/images/image-01.png)
- and save the configuration


Now you can start interacting with the number set on Twilio.

## Usage

- The dialog files are listed in [data/dialog](./data/dialog/).
- The dialogue is divided 2: a [**courtesy**](./data/dialog/courtesy/) and a [**questions**](./data/dialog/questions/).
- The [**0.json**](./data/dialog/questions/0.json) file allows you to set up words or phrases that will redirect the user to a folder in case of a free question. If in the user's answer, the words do not match the setting, all the folders will be listed.
- The [**0.json**](./data/dialog/questions/0.json) file also contains words that the chatbot would not admit such as misplaced words, degrading words, etc.
- You must have at least ONE file in courtesy for the chatbot to function properly.
- For the chatbot to send multiple messages to the successively, you must use the  **|** like separator
- No input check is made for the dialogue that is in the courtesy folder.
- A dialog file containing a choice in the answer, the answer must be numbered from 1 in ascending order.
- Some verification operations are done for the dialogue is in the file question: *check_noun*, *check_str*, *check_number*, *check_phonenumber*, *check_city*, *check_email*, *select*, *map*, *generate_qrcode*, *calendar*.
- There is an operation that selects items in databases and cross-references as choices. You must well configure the database before.
- Operations listed above don't work yet on dialogs listed in courtesy.
