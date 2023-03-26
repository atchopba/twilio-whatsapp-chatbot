#!/usr/bin/python
from config import Config
import logging
from twilio_whatsapp_bot.core.utilies.operation import Operation
from twilio_whatsapp_bot.core.db.answers import Answers
from twilio_whatsapp_bot.core.helpers import get_file_content, get_list_files, load_json_file, check_probability_and_return_folder, get_operations_in_bot_dialog, clean_question_content
from typing import Any


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

COURTESY_STR = "courtesy"
QUESTION_STR = "question"

BAD_ANSWER_STR = "*"+ Config.BAD_ANSWER_STR + "*"
BAD_ANSWER_CHOICE_STR = "*"+ Config.BAD_ANSWER_CHOICE_STR + "*"

PATHDIR_DIALOG = "./data/dialog"
PATHDIR_QUESTIONS =  "./data/dialog/questions"

user_responses = {}

list_files = get_list_files(PATHDIR_DIALOG)
is_last_dialog = False

previous_step_str = "courtesy"
is_change_folder = False


def step_question(index: int) -> str:
    global current_step, user_responses, is_last_dialog, list_files
    list_files_size = len(list_files)
    quote = ""
    # verify if the index is the last question
    if index == list_files_size - 1:
        logging.info("the last question of the dialog")
        is_last_dialog = True
        quote = get_file_content(list_files[list_files_size - 1]).replace("{}", user_responses[list_files_size - 2].upper())
        # store data in DB
        Answers().insert_data(user_responses)
        logging.info("Saving OK for the data")
    elif index == list_files_size:
        is_last_dialog = True 
    else:
        # if index = 0 => reload list_files to reinitialize dialog
        if index == 0:
            list_files = get_list_files(PATHDIR_DIALOG)
        #
        is_last_dialog = False
        current_step = index
        quote = clean_question_content(get_file_content(list_files[index]))
    return quote


def step_response(incoming_msg: str) -> str:
    global current_step, user_responses, previous_step_str, is_last_dialog
    response_msg = incoming_msg.strip()
    current_file = list_files[current_step]
    quote = ""
    
    # if question is a courtesy
    if (current_step == 0 or COURTESY_STR in current_file) and not is_change_folder:
        quote = step_in_courtesy(response_msg)
        logging.info("Dialog is a courtesy")
    # else
    elif QUESTION_STR in current_file:
        quote = step_in_question(response_msg)
        previous_step_str = QUESTION_STR
        logging.info("Dialog is a question")
    
    return {
        "quote" : quote,
        "is_last_dialog" : is_last_dialog
    }


def step_in_courtesy(response_msg: str) -> str:
    global current_step, user_responses, list_files, is_change_folder, is_question
    user_responses[current_step] = response_msg
    next_courtesy_content = get_file_content(list_files[current_step + 1])
    next_file = list_files[current_step + 1]
    
    # check if the content contains {} to replace with the response
    if ("{}" in next_courtesy_content):
        next_courtesy_content = next_courtesy_content.replace("{}", response_msg)
    #
    current_step += 1
    
    # check if the previous step is courtesy
    if COURTESY_STR not in next_file and not is_change_folder:
        is_change_folder = True
        folder_question = check_probability_and_return_folder(response_msg, load_json_file())
        # reload list_files
        list_files = get_list_files(PATHDIR_QUESTIONS + "/" + str(folder_question))
        current_step = 0

        next_courtesy_content = get_file_content(list_files[current_step])

    return next_courtesy_content


def step_in_question(response_msg: str) -> str:
    global current_step, user_responses
    quote = ""
    current_file = list_files[current_step]
    current_file_content = get_file_content(current_file)
    # get operations
    tmp_ = get_operations_in_bot_dialog(current_file_content)
    operations = tmp_['operations_found']
    current_file_content = tmp_['msg']

    # get nb of line of the current file
    nb_lines = len(current_file_content.split("\n"))

    # if file is on 1 line, get the answer and next question
    if nb_lines == 1:
        if not check_msg_validity(response_msg, operations):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
        else:
            user_responses[current_step] = response_msg
            quote = step_question(current_step + 1)
    # nb line > 1, many possibilities of responses
    else:
        if response_msg.isnumeric() and 1 <= int(response_msg) <= nb_lines-1:
            user_responses[current_step] = response_msg
            quote = step_question(current_step + 1)
        elif not check_msg_validity(response_msg, operations):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
        else:
            current_step = current_step
            quote = BAD_ANSWER_CHOICE_STR + "\n\n" + current_file_content
    return quote


def check_msg_validity(msg: str, operation: Any) -> bool:
    tmp_ = Operation().run(operation, msg)
    logging.info("Check validity of the user response (%s)", tmp_)
    return tmp_
