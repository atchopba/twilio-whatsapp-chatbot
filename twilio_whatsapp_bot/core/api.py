#!/usr/bin/python
from twilio_whatsapp_bot.core.db.answers import Answers
from twilio_whatsapp_bot.core.helpers import get_file_content, get_list_files


BAD_ANSWER_STR = "mauvais choix de réponse"
PATHDIR_DIALOG = "./data/dialog"
user_responses = {}

list_files = get_list_files(PATHDIR_DIALOG)
is_last_dialog = False


def step_question(index: int) -> str:
    global current_step, user_responses, is_last_dialog
    list_files_size = len(list_files)
    # verify if the index is the last question
    if index == list_files_size - 1:
        is_last_dialog = True
        quote = get_file_content(list_files[list_files_size - 1]).replace("{}", user_responses[list_files_size - 2].upper())
        # store data in DB
        Answers().insert_data(user_responses)
    else:
        is_last_dialog = False
        current_step = index
        quote = get_file_content(list_files[index])
    return quote


def step_response(incoming_msg: str) -> str:
    global current_step, user_responses, is_last_dialog
    response_msg = incoming_msg.strip()
    current_file = list_files[current_step]
    is_question = False
    # if question is a courtesy
    if current_step == 0 or "courtesy" in current_file:
        quote = step_in_courtesy(response_msg)
    # else
    elif "question" in current_file:
        quote = step_in_question(response_msg)
    return {
        "quote" : quote,
        "is_last_dialog" : is_last_dialog
    }


def step_in_courtesy(response_msg: str) -> str:
    global current_step, user_responses
    user_responses[current_step] = response_msg
    next_courtesy_content = get_file_content(list_files[current_step + 1])
    # check if the content contains {} to replace with the response
    if ("{}" in next_courtesy_content):
        next_courtesy_content = next_courtesy_content.replace("{}", response_msg)
    #
    current_step += 1
    return next_courtesy_content


def step_in_question(response_msg: str) -> str:
    global current_step, user_responses
    quote = ""
    current_file = list_files[current_step]
    # get nb of line of the current file
    nb_lines = len(get_file_content(current_file).split("\n"))
    # if file is on 1 line, get the answer and next question
    if nb_lines == 1:
        user_responses[current_step] = response_msg
        quote = step_question(current_step + 1)
    # nb line > 1, many possibilities of responses
    else:
        if response_msg.isnumeric() and 1 <= int(response_msg) <= nb_lines-1:
            user_responses[current_step] = response_msg
            quote = step_question(current_step + 1)
        else:
            current_step = current_step
            quote = BAD_ANSWER_STR
    return quote
