#!/usr/bin/python
from config import Config
from twilio_whatsapp_bot.core.utilies.data import \
    clean_data_from_question_content, get_datas_in_bot_dialog
from twilio_whatsapp_bot.core.utilies.operation import Operation
from twilio_whatsapp_bot.core.utilies.functions import make_new_token, \
    get_operations_in_bot_dialog, update_payment_data, get_operations_by_type
from twilio_whatsapp_bot.core.utilies.folder import Folder
from twilio_whatsapp_bot.core.helpers import change_filepath, \
    check_content_is_2_msg, check_folder_exists, count_nb_folders, \
    get_file_content, get_list_files, is_question_without_choice, \
    load_json_file, remove_accents, replace_words_in_content, \
    available_answers, translate_msg, get_list_available_answer_run_out, \
    is_part, get_payment_token
from typing import Any


LANG_FR = "fr"
LANG_EN = "en"

COURTESY_STR = "courtesy"
QUESTION_STR = "question"

BAD_ANSWER_STR = "*" + Config.BAD_ANSWER_STR + "*"
BAD_ANSWER_CHOICE_STR = "*" + Config.BAD_ANSWER_CHOICE_STR + "*"
PROPOSE_ALL_QUESTIONS_FOLDER_STR = ("_" + Config.PROPOSE_ALL_QUESTIONS_FOLDER_STR + "_") # noqa

DIALOG_ASSISTANT = Config.DIALOG_ASSISTANT if (
    Config.DIALOG_ASSISTANT is not None) else "David"

PATHDIR_TO_DIALOG = Config.PATH_TO_DIALOG if (
    check_folder_exists(Config.PATH_TO_DIALOG)) else "./data/dialog"
PATHDIR_TO_QUESTIONS = PATHDIR_TO_DIALOG + "//questions"

GOOGLE_MAPS_API_KEY = Config.GOOGLE_MAPS_API_KEY

DEFAULT_MAPS_LOCATION_ERROR = Config.DEFAULT_MAPS_LOCATION_ERROR

DEFAULT_MAPS_NO_RESULT = Config.DEFAULT_MAPS_NO_RESULT

DEFAULT_COUNTRY = Config.DEFAULT_COUNTRY

DEFAULT_MOMO_URL = Config.DEFAULT_MOMO_URL

DEFAULT_PAYMENT_VALIDATED_STR = Config.DEFAULT_PAYMENT_VALIDATED_STR

BUSINESS_NAME = Config.BUSINESS_NAME

BUSINESS_GEOLOCATE_SENTENCE = Config.BUSINESS_GEOLOCATE_SENTENCE

IS_SAVE_IN_DB = True if Config.IS_SAVE_IN_DB.lower() == "true" else False

IS_RESPONSE_ALPHA = True if Config.IS_RESPONSE_ALPHA.lower() == "true" else False # noqa

LIST_AVAILABLE_ANSWERS_RUN_OUT = get_list_available_answer_run_out(IS_RESPONSE_ALPHA) # noqa

user_responses = []

list_files = get_list_files(PATHDIR_TO_DIALOG)
is_last_dialog = False
user_token = None
payment_token = None

previous_step_str = "courtesy"
propose_all_questions_folder = ""
is_change_folder = False
is_global_question = False
is_words_question = False
is_save_question = False
is_external_link = False
is_next_external_link = False
next_step_for_external_link = None
save_operation = None
is_map_location = False
map_user_geolocalisation = None
nb_folder_question = 0
is_run_out = False
run_out_question_part = ""
is_run_calendar_add = False
is_calendar_list_days_to_reserve = False
array_run_calendar_days_proposal = []
array_run_calendar_times_proposal = []
array_operation_saving_params = {}
current_step = 0
language = LANG_FR
list_answers_run_out = []
url_qrcode = None

# If you have only 1 question directory for dialogue, please keep only 1 file
# in the courtesy directory for the proper functioning of the chatbot
is_unique_question_folder = True if (
    count_nb_folders(PATHDIR_TO_QUESTIONS) == 1) else False


def step_question(index: int, response_msg: str = "") -> str:
    global current_step, current_file, is_change_folder, is_global_question, \
        is_last_dialog, is_run_out, list_files, run_out_question_part, \
        user_responses, list_answers_run_out, is_run_calendar_add, \
        array_run_calendar_days_proposal, array_run_calendar_times_proposal, \
        is_calendar_list_days_to_reserve, user_token, is_save_question, \
        save_operation, url_qrcode
    list_files_size = len(list_files)
    quote = ""
    #
    tmp_ = get_operations_in_bot_dialog(get_file_content(list_files[0])) # noqa
    # check if operation is save
    save_operation = get_operations_by_type(tmp_['operations_found'], 'save')
    if save_operation:
        is_save_question = Operation().is_run_save(save_operation)

    # if index = 0, make a user_token
    if index == 0 and not user_token and user_token  != "": # noqa
        user_token = make_new_token()

    # verify if the index is the last question
    if index == list_files_size - 1:
        is_last_dialog = True
        is_change_folder = False
        quote = get_file_content(list_files[list_files_size - 1])
        quote = quote.replace("{}", response_msg.upper())
        # store data in DB
        # if IS_SAVE_IN_DB:
        #    Answers().insert_data(user_responses)

    elif index == list_files_size:
        is_last_dialog = True
        is_change_folder = False
        # store data in DB
        # if IS_SAVE_IN_DB:
        #    Answers().insert_data(user_responses)
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
        operation_out = get_operations_by_type(tmp_["operations_found"], 'out')
        if (operation_out is not None
                and Operation().is_run_out(operation_out)):
            run_out_list = Operation().run_out(user_token, operation_out, LIST_AVAILABLE_ANSWERS_RUN_OUT) # noqa
            #
            if 'url_qrcode' in run_out_list and run_out_list['url_qrcode'] is not None and run_out_list['url_qrcode'] != "": # noqa
                # url_qrcode = run_out_list['url_qrcode']
                url_qrcode = "https://thierryo.github.io/qrcode/reference/figures/example-1.png" # noqa
            is_run_out = True
            run_out_question_part = "\n" + "\n".join(run_out_list["array"]) # noqa
            quote += run_out_question_part
            list_answers_run_out = available_answers(quote)
            #
            if (Operation().is_run_calendar_add(operation_out)):
                array_run_calendar_times_proposal = run_out_list["proposal"]
                is_run_calendar_add = True
                is_run_out = False
            if run_out_list["is_calendar_list_days_to_reserve"] is True:
                array_run_calendar_days_proposal = run_out_list["proposal"]
    #
    return quote


def step_response(incoming_msg: str) -> Any:
    global current_step, user_responses, previous_step_str, \
        is_unique_question_folder, is_last_dialog, \
        is_words_question, list_files, is_global_question, is_save_question, \
        save_operation, language, is_map_location, is_run_calendar_add, \
        array_run_calendar_days_proposal, array_run_calendar_times_proposal, \
        array_operation_saving_params, user_token, payment_token, \
        is_external_link, next_step_for_external_link, is_next_external_link, \
        url_qrcode
    #
    response_msg = incoming_msg.strip()
    # if the answer came after an external link
    if is_external_link:
        # if you are coming from payment
        if is_part(response_msg, DEFAULT_PAYMENT_VALIDATED_STR):
            payment_token = get_payment_token(response_msg)
            # update the row in table user_payments
            update_payment_data(user_token, payment_token)
        #
        current_step = next_step_for_external_link
        is_external_link = False
        is_next_external_link = True

    #
    current_file = list_files[current_step]
    quote = ""
    media_list = []
    user_responses.append({
        "response": response_msg,
        "file": change_filepath(current_file)
    })

    # if the question needing answer required saving
    if is_save_question and save_operation:
        save_params(save_operation, user_token, response_msg, IS_RESPONSE_ALPHA) # noqa
        array_operation_saving_params[save_operation["param"]] = response_msg
        is_save_question = False
        save_operation = None
    #
    is_map_location_tmp = False
    locations = []
    # if the question needing a location
    if is_map_location:
        locations = Operation().run_map(
            user_token,
            GOOGLE_MAPS_API_KEY,
            incoming_msg,
            DEFAULT_COUNTRY,
            BUSINESS_NAME
        )
        if locations is None:
            quote_tmp = DEFAULT_MAPS_LOCATION_ERROR
        elif len(locations) == 0:
            quote_tmp = DEFAULT_MAPS_NO_RESULT
        else:
            quote_tmp = BUSINESS_GEOLOCATE_SENTENCE + "\n" + "\n".join(locations) # noqa
        is_map_location_tmp = True

    # calendar add event
    if is_run_calendar_add:
        index_booking_day = user_responses[len(user_responses)-2]["response"]
        tmp_booking_day = array_run_calendar_days_proposal[index_booking_day].split(" ")[1] # noqa
        tmp_booking_time = array_run_calendar_times_proposal[response_msg].split("-") # noqa
        # create event
        Operation().run_calendar_add(
            user_token,
            array_operation_saving_params['name'],
            tmp_booking_day,
            tmp_booking_time[0].strip(),
            tmp_booking_time[1].strip()
        )
        is_run_calendar_add = False

    # if question is a courtesy
    if (
        (((current_step == 0 or COURTESY_STR in current_file)
          and not is_change_folder) or is_words_question)
        and not is_unique_question_folder
    ):
        quote = step_in_courtesy(response_msg)
        quote = insert_qrcode(quote, url_qrcode)
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
        quote = insert_qrcode(quote, url_qrcode)
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

    # check if the question has an external link
    if is_part(quote, "{MOMO_URL}"):
        is_external_link = True
        next_step_for_external_link = current_step + 1
    #
    quote = replace_words_in_content(quote, "{ASSISTANT}", DIALOG_ASSISTANT)
    quote = replace_words_in_content(quote, "{MOMO_URL}", DEFAULT_MOMO_URL)
    quote = replace_words_in_content(quote, "{USER_TOKEN}", user_token)
    #
    check_content_msg = check_content_is_2_msg(quote)
    #
    tokens_msg = translate_msg(check_content_msg["tokens"], LANG_FR, language)
    # verify if we are in the case of location
    if is_map_location_tmp:
        is_map_location = False
        tokens_msg = [quote_tmp] + tokens_msg
    #
    return {
        "tokens": tokens_msg,
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
        propose_all_questions_folder, is_save_question, save_operation, \
        user_token, next_step_for_external_link

    next_file = ""

    if not is_words_question or is_unique_question_folder:
        tmp_ = get_operations_in_bot_dialog(get_file_content(list_files[current_step + 1])) # noqa
        # check if operation is save
        save_operation = get_operations_by_type(tmp_['operations_found'], 'save') # noqa
        if save_operation:
            is_save_question = Operation().is_run_save(save_operation)
        #
        next_courtesy_content = tmp_['msg']
        next_file = list_files[current_step + 1]
        # check if the content contains {} to replace with the response
        if ("{}" in next_courtesy_content):
            next_courtesy_content = next_courtesy_content.replace(
                "{}", response_msg.title()
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
            tmp_ = get_operations_in_bot_dialog(get_file_content(list_files[current_step])) # noqa
            save_operation = get_operations_by_type(tmp_['operations_found'], 'save') # noqa
            is_save_question = Operation().is_run_save(save_operation)
            next_courtesy_content = tmp_['msg']
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
    global current_step, is_words_question, is_run_out, \
        run_out_question_part, is_map_location, list_answers_run_out, \
        is_next_external_link
    quote = ""
    current_file = list_files[current_step]
    current_file_content = get_file_content(current_file)
    # get operations
    tmp_ = get_operations_in_bot_dialog(current_file_content)
    operations = tmp_['operations_found']
    current_file_content = tmp_['msg']

    # check if the operation is map location
    try:
        tmp_2 = get_operations_in_bot_dialog(get_file_content(list_files[current_step+1])) # noqa
        is_map_location = Operation().is_run_map(get_operations_by_type(tmp_2["operations_found"], 'map')) # noqa
    except IndexError:
        is_map_location = False

    is_run_map = get_operations_by_type(operations, 'map')

    list_response_msg = [response_msg.lower(), response_msg.upper()]
    # get nb of line of the current file
    nb_lines = len(current_file_content.split("\n"))

    # if file is on 1 line, get the answer and next question
    if nb_lines == 1 or is_question_without_choice(current_file_content):
        is_contain_op_in = False
        is_contain_op_out = False
        if (operations != "" and operations is not None):
            operation_in = get_operations_by_type(operations, 'in')
            operation_out = get_operations_by_type(operations, 'out')
            #
            if Operation().is_run_in(operation_in):
                if not check_msg_validity(response_msg, operation_in):
                    current_step = current_step
                    quote = BAD_ANSWER_STR + "\n\n" + current_file_content
                    is_contain_op_in = True
                else:
                    pass
            elif (not is_contain_op_in and Operation().is_run_out(operation_out) # noqa
                    and not (any(x in list_response_msg for x in list_answers_run_out))): # noqa
                current_step = current_step
                quote = BAD_ANSWER_STR + "\n\n" + current_file_content
                quote += run_out_question_part
                is_contain_op_out = True

        if not is_contain_op_in and not is_contain_op_out:
            quote = step_question(current_step + 1, response_msg)
    # nb line > 1, many possibilities of responses
    else:
        # if made by request
        if is_run_out and (
            any(x in list_response_msg for x in list_answers_run_out)
        ):
            is_run_out = False
            quote = step_question(current_step + 1, response_msg)
        elif response_msg in available_answers(current_file_content):
            quote = step_question(current_step + 1, response_msg)
        elif is_run_map:
            quote = step_question(current_step + 1, response_msg)
            is_run_map = False
        elif (operations != "" and operations is not None
              and Operation().is_run_in(operations)
              and not check_msg_validity(response_msg, operations)):
            current_step = current_step
            quote = BAD_ANSWER_STR + "\n\n" + current_file_content
        elif is_words_question:
            is_words_question = False
            current_step = current_step
            quote = current_file_content
        elif is_next_external_link:
            is_next_external_link = False
            current_step = next_step_for_external_link
            quote = current_file_content
        else:
            current_step = current_step
            quote = BAD_ANSWER_CHOICE_STR + "\n\n" + current_file_content
    return quote


def check_msg_validity(msg: str, operation: Any) -> bool:
    tmp_ = Operation().run_in(operation, msg)
    return tmp_


def save_params(operation: Any, user_token: str, response_msg: str, is_response_alpha: bool = False) -> bool: # noqa
    global language
    # save the param in the DB
    tmp_ = Operation().run_save(operation, user_token, response_msg)
    #
    if tmp_ is not None and "param" in tmp_ and tmp_["param"] == "lang":
        language = LANG_EN if (
            (not is_response_alpha and response_msg == "2")
            or (is_response_alpha and response_msg.lower() == "b")
        ) else LANG_FR


def insert_qrcode(quote: str, url_qrcode: str) -> None:
    if is_part(quote, "{URL_QRCODE}"):
        quote = replace_words_in_content(quote, "{URL_QRCODE}", url_qrcode)
    return quote
