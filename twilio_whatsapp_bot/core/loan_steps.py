# -*- coding: utf-8 -*-
from typing import Any


DEVISE = "Fcfa"
BAD_ANSWER_STR = "mauvaise réponse"


def step_response(incoming_msg: str) -> str:
    global previous_step
    quote = ""
    response_ = incoming_msg.lower().strip()
    # 
    if previous_step == 1:
        if response_ not in { "1", "2", "3", "4", "5" }:
            quote = BAD_ANSWER_STR
        else:
            quote = step_second()
    elif previous_step == 2:
        if response_ not in { "a", "b", "c", "d", "e" }:
            quote = BAD_ANSWER_STR
        else:
            quote = step_third()
    else:
        quote = "l'étape précédente n'a pas été enregistrée"
    return quote


def step_first() -> str:
    global previous_step
    # initialize previous step
    previous_step = 1
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
    global previous_step
    # initialize previous step
    previous_step = 2
    # make question
    quote = "En combien de temps comptez-vous rembourser? \n"
    quote += "A. 5 ans \n"
    quote += "B. 4 ans \n"
    quote += "C. 3 ans \n"
    quote += "D. 2 ans \n"
    quote += "E. 1 ans "
    return quote


def step_third() -> str:
    global previous_step
    # initialize previous step
    previous_step = 3
    # make question
    quote = "Avez-vous des garanties? \n"
    quote += "1. Oui \n"
    quote += "2. Non \n"
    return quote
