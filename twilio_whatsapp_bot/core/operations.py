#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2023 atchopba
"""
def execute_standard_operation(operation: str, msg_2_check: str) -> bool:
    return_ = False
    operation = operation.replace("[", "").replace("]", "").replace(" ", "")
    if operation == "CHECK_PHONENUMBER":
        return_ = check_phonenumber(msg_2_check)
    elif operation == "CHECK_MUNICIPALITY":
        pass
    elif operation == "CHECK_NUMBER":
        return_ = check_number(msg_2_check)
    elif operation == "CHECK_STR":
        return_ = check_str(msg_2_check)
    elif operation == "CHECK_NOUN":
        return_ = check_noun(msg_2_check)
    #
    return return_


def check_number(msg_2_check: str) -> bool:
    return msg_2_check is not None and msg_2_check.isnumeric()


def check_str(msg_2_check: str) -> bool:
    return isinstance(msg_2_check, str) and any(ele in msg_2_check for ele in ["a", "e", "i", "o", "u", "y"])


def check_noun(msg_2_check: str) -> bool:
    return check_str(msg_2_check)


def check_phonenumber(msg_2_check: str) -> bool:
    import phonenumbers
    from phonenumbers import carrier
    from phonenumbers.phonenumberutil import number_type
    #
    if not msg_2_check.startswith("+"):
        msg_2_check = "+237" + msg_2_check
    #
    return carrier._is_mobile(number_type(phonenumbers.parse(msg_2_check)))
    