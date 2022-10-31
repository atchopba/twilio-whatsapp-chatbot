#!/usr/bin/python
from twilio_whatsapp_bot.core.db.answers import Answers
from twilio_whatsapp_bot.core.helpers import get_file_content, get_list_files


BAD_ANSWER_STR = "mauvais choix de réponse"
PATHDIR_QUESTIONS = "./data/questions"
user_responses = {}

list_files = get_list_files(PATHDIR_QUESTIONS)


def step_question(index: int) -> str:
    global current_step, user_responses
    # verify if the index is the last question
    tmp_file = str(index) + ".txt"
    if tmp_file == list_files[len(list_files)-2]:
        quote = get_file_content(PATHDIR_QUESTIONS + "/z.txt").replace("%s", user_responses[4].upper())
    else:
        current_step = index
        quote = get_file_content(PATHDIR_QUESTIONS + "/" + list_files[index])
    return quote


def step_response(incoming_msg: str) -> str:
    global current_step, user_responses
    response_ = incoming_msg.strip()
    current_file = PATHDIR_QUESTIONS + "/" + str(current_step) + ".txt"
    # get nb of line of the current file
    nb_lines = len(get_file_content(current_file).split("\n"))
    # if file is on 1 line, get the answer and next question
    if nb_lines == 1:
        user_responses[current_step] = response_
        quote = step_question(current_step + 1)
    # nb line > 1, many possibilities of responses
    else:
        if response_.isnumeric() and 1 <= int(response_) <= nb_lines-1:
            user_responses[current_step] = response_
            quote = step_question(current_step + 1)
        else:
            current_step = current_step
            quote = BAD_ANSWER_STR
    return quote
