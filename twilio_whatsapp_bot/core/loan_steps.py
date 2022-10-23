# -*- coding: utf-8 -*-
from typing import Any


DEVISE = "Fcfa"
BAD_ANSWER_STR = "mauvaise réponse"
user_responses = {}

def step_response(incoming_msg: str) -> str:
    global current_step, user_responses
    quote = ""
    response_ = incoming_msg.strip()
    # 
    if current_step == 1:
        if response_ not in { "1", "2", "3", "4", "5" }:
            quote = BAD_ANSWER_STR
        else:
            user_responses[current_step] = response_
            quote = step_second()
    elif current_step == 2:
        if response_ not in { "a", "b", "c", "d", "e" }:
            quote = BAD_ANSWER_STR
        else:
            user_responses[current_step] = response_
            quote = step_three()
    elif current_step == 3:
        if response_ not in { "1", "2" }:
            quote = BAD_ANSWER_STR
        else:
            user_responses[current_step] = response_
            quote = step_four()
    elif current_step == 4:
        # check name
        response_tokens = response_.split(" ")
        if response_.isnumeric() or len(response_tokens[0]) > 10:
            quote = BAD_ANSWER_STR
        else:
            user_responses[current_step] = response_
            quote = step_five()
    elif current_step == 5:
        # check phone number
        if not response_.isnumeric():
            quote = BAD_ANSWER_STR
        else:
            user_responses[current_step] = response_
            quote = step_six()
    elif current_step == 6:
        # check city & municipality
        if response_.isnumeric(): 
            quote = BAD_ANSWER_STR
        else:
            quote = "Merci pour vos réponses, M./Mme %s. Nous rentrerons en contact avec vous sous un délai de 48h maximum." % (user_responses[4].upper())
    else:
        quote = "l'étape précédente n'a pas été enregistrée"
    return quote


def step_first() -> str:
    global current_step
    # initialize previous step
    current_step = 1
    # make question 
    quote = "Quel montant souhaitez-vous emprunter? \n"
    quote += "1. 5 millions %s \n"  % (DEVISE)
    quote += "2. 2 millions %s \n" % (DEVISE)
    quote += "3. 1 million %s \n" % (DEVISE)
    quote += "2. 500 000 %s \n" % (DEVISE)
    quote += "3. 200 000 %s \n" % (DEVISE)
    quote += "5. 100 000 %s" % (DEVISE)
    return quote


def step_second() -> str:
    global current_step
    # initialize previous step
    current_step = 2
    # make question
    quote = "En combien de temps comptez-vous rembourser? \n"
    quote += "A. 5 ans \n"
    quote += "B. 4 ans \n"
    quote += "C. 3 ans \n"
    quote += "D. 2 ans \n"
    quote += "E. 1 ans "
    return quote


def step_three() -> str:
    global current_step
    # initialize previous step
    current_step = 3
    # make question
    quote = "Avez-vous des garanties? \n"
    quote += "1. Oui \n"
    quote += "2. Non \n"
    return quote


def step_four() -> str:
    global current_step
    # initialize previous step
    current_step = 4
    # make question
    quote = "Vos nom(s) et prénom(s):"
    return quote


def step_five() -> str:
    global current_step
    # initialize previous step
    current_step = 5
    # make question
    quote = "Votre numéro de téléphone"
    return quote


def step_six() -> str:
    global current_step
    # initialize previous step
    current_step = 6
    # make question
    quote = "Votre quartier de résidence / commune"
    return quote
