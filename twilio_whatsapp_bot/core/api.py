#!/usr/bin/python
from config import Config
from twilio_whatsapp_bot.core.utilies.data import \
    clean_data_from_question_content, get_datas_in_bot_dialog
from twilio_whatsapp_bot.core.utilies.operation import Operation, \
    get_operations_in_bot_dialog
from twilio_whatsapp_bot.core.db.answers import Answers
from twilio_whatsapp_bot.core.utilies.folder import Folder
from twilio_whatsapp_bot.core.helpers import change_filepath, \
    check_content_is_2_msg, check_folder_exists, count_nb_folders, \
    get_file_content, get_list_files, is_question_without_choice, \
    load_json_file, remove_accents, replace_assistant_in_content
from typing import Any


COURTESY_STR = "courtesy"
QUESTION_STR = "question"

BAD_ANSWER_STR = "*" + Config.BAD_ANSWER_STR + "*"
BAD_ANSWER_CHOICE_STR = "*" + Config.BAD_ANSWER_CHOICE_STR + "*"
PROPOSE_ALL_QUESTIONS_FOLDER_STR = ("_"
                                    + Config.PROPOSE_ALL_QUESTIONS_FOLDER_STR
                                    + "_")

DIALOG_ASSISTANT = Config.DIALOG_ASSISTANT if (
    Config.DIALOG_ASSISTANT is not None) else "David"

PATHDIR_TO_DIALOG = Config.PATH_TO_DIALOG if (
    check_folder_exists(Config.PATH_TO_DIALOG)) else "./data/dialog"
PATHDIR_TO_QUESTIONS = PATHDIR_TO_DIALOG + "//questions"

user_responses = {}

list_files = get_list_files(PATHDIR_TO_DIALOG)
is_last_dialog = False

previous_step_str = "courtesy"
propose_all_questions_folder = ""
is_change_folder = False
is_global_question = False
is_words_question = False
nb_folder_question = 0
nb_rows_run_out = -1
is_run_out = False
run_out_question_part = ""
current_step = 0

# If you have only 1 question directory for dialogue, please keep only 1 file
# in the courtesy directory for the proper functioning of the chatbot
is_unique_question_folder = True if (
    count_nb_folders(PATHDIR_TO_QUESTIONS) == 1) else False


def step_question(index: int, response_msg: str = "") -> str:
    global current_step, current_file, is_change_folder, is_global_question, \
        is_last_dialog, is_run_out, list_files, nb_rows_run_out, \
        run_out_question_part, user_responses
    list_files_size = len(list_files)
    quote = ""
    # verify if the index is the last question
    if index == list_files_size - 1:
        is_last_dialog = True
        is_change_folder = False
        quote = get_file_content(list_files[list_files_size - 1])
        quote = quote.replace("{}", response_msg.upper())
        # store data in DB
        Answers().insert_data(user_responses)

    elif index == list_files_size:
        is_last_dialog = True
        is_change_folder = False
        # store data in DB
        Answers().insert_data(user_responses)
    else:
        # if index = 0 => reload list_files to reinitialize dialog
        if index == 0 and not is_global_question:
            list_files = get_list_files(PATHDIR_TO_DIALOG)
        else:
            is_global_question = False
        #
        is_last_dialog = False
        current_step = index
        current_file = list_files[index]
        #
        tmp_ = get_operations_in_bot_dialog(get_file_content(current_file))
        quote = tmp_["msg"]
        #
        if ("operations_found" in tmp_ 
                and tmp_["operations_found"] is not None
                and Operation().is_run_out(tmp_["operations_found"])):
            run_out_list = Operation().run_out(tmp_["operations_found"])
            nb_rows_run_out = len(run_out_list)
            #
            is_run_out = True
            run_out_question_part = "\n" + "\n".join(run_out_list)
            quote += run_out_question_part

    return quote


def step_response(incoming_msg: str) -> Any:
    global current_step, user_responses, previous_step_str, \
        is_unique_question_folder, is_last_dialog, \
        is_words_question, list_files, is_global_question
    response_msg = incoming_msg.strip()
    current_file = list_files[current_step]
    quote = ""
    media_list = []
    user_responses[change_filepath(current_file)] = response_msg

    # if question is a courtesy
    if (
        (((current_step == 0 or COURTESY_STR in current_file)
          and not is_change_folder) or is_words_question)
        and not is_unique_question_folder
    ):
        quote = step_in_courtesy(response_msg)
        #
        media_list = get_datas_in_bot_dialog(quote)
        quote = clean_data_from_question_content(quote)
        #
    # else
    elif (
            (QUESTION_STR in current_file and not is_global_question)
            or is_unique_question_folder
    ):
        quote = step_in_question(response_msg)
        #
        media_list = get_datas_in_bot_dialog(quote)
        quote = clean_data_from_question_content(quote)
        #
        previous_step_str = QUESTION_STR
    # if it is global question case
    elif is_global_question:
        #
        if (
            incoming_msg.isnumeric() and
            1 <= int(incoming_msg) <= nb_folder_question
        ):
            list_files = get_list_files(
                PATHDIR_TO_QUESTIONS + "/" + str(incoming_msg)
            )
            quote = step_question(0)
        else:
            quote = BAD_ANSWER_CHOICE_STR + "\n\n"
            quote += propose_all_questions_folder
    #
    quote = replace_assistant_in_content(quote, DIALOG_ASSISTANT)
    #
    check_content_msg = check_content_is_2_msg(quote)
    #
    return {
        "tokens": check_content_msg["tokens"],
        "is_in_2_msg": check_content_msg["is_in_2_msg"],
        "is_last_dialog": is_last_dialog,
        "media": media_list["datas_found"] if (
                media_list is not None
                and "datas_found" in media_list
                and media_list["datas_found"] is not None
                and len(media_list["datas_found"]) > 0
            ) else []
    }


def step_in_courtesy(response_msg: str) -> str:
    global current_step, list_files, is_change_folder, is_global_question, \
        is_unique_question_folder, is_words_question, nb_folder_question, \
        propose_all_questions_folder
    next_file = ""

    if not is_words_question or is_unique_question_folder:
        next_courtesy_content = get_file_content(list_files[current_step + 1])
        next_file = list_files[current_step + 1]
        # check if the content contains {} to replace with the response
        if ("{}" in next_courtesy_content):
            next_courtesy_content = next_courtesy_content.replace(
                "{}", response_msg
            )
        current_step += 1

    # check if the previous step is courtesy
    if ((COURTESY_STR not in next_file and not is_change_folder)
            or is_words_question):
        is_change_folder = True
        folder_ = Folder(load_json_file(PATHDIR_TO_QUESTIONS + "//0.json"))
        response_question = folder_.check_probability_and_return_folder(
            remove_accents(response_msg)
        )
        folder_index = response_question["folder_index"]
        question_ = response_question["question"]

        # if the user's response matches a directory
        if folder_index > -1 and (question_ is None or question_ == ""):
            # reload list_files
            list_files = get_list_files(
                PATHDIR_TO_QUESTIONS + "/" + str(folder_index)
            )
            current_step = 0
            is_words_question = False
            #
            next_courtesy_content = get_file_content(list_files[current_step])
        #
        elif folder_index == -1 and question_ is not None and question_ != "":
            next_courtesy_content = question_
            is_words_question = True
        # else, propose all directory
        else:
            is_words_question = False
            is_global_question = True
            global_question_as_default = folder_.get_folders_as_default()
            nb_folder_question = len(global_question_as_default)
            next_courtesy_content = PROPOSE_ALL_QUESTIONS_FOLDER_STR + "\n\n"
            next_courtesy_content += "\n".join(global_question_as_default)
            propose_all_questions_folder = next_courtesy_content
    #
    return next_courtesy_content


def step_in_question(response_msg: str) -> str:
    global current_step, is_words_question, is_run_out, nb_rows_run_out, \
        run_out_question_part
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
    if nb_lines == 1 or is_question_without_choice(current_file_content):
        if (operations != "" and operations is not None
                and Operation().is_run_in(operations)
                and not check_msg_validity(response_msg, operations)):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
        elif (operations != "" and operations is not None
              and Operation().is_run_out(operations)
              and not (1 <= int(response_msg) <= nb_rows_run_out)):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
            quote += run_out_question_part
        else:
            quote = step_question(current_step + 1, response_msg)
    # nb line > 1, many possibilities of responses
    else:
        # if made by request
        if is_run_out and 1 <= int(response_msg) <= nb_rows_run_out:
            is_run_out = False
            quote = step_question(current_step + 1, response_msg)
        elif response_msg.isnumeric() and 1 <= int(response_msg) <= nb_lines-1:
            quote = step_question(current_step + 1, response_msg)
        elif (operations != "" and operations is not None
              and Operation().is_run_in(operations)
              and not check_msg_validity(response_msg, operations)):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
        elif is_words_question:
            is_words_question = False
            current_step = current_step
            quote = current_file_content
        else:
            current_step = current_step
            quote = BAD_ANSWER_CHOICE_STR + "\n\n" + current_file_content
    return quote


def check_msg_validity(msg: str, operation: Any) -> bool:
    tmp_ = Operation().run_in(operation, msg)
    return tmp_
