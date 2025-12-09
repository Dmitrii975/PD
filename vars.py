# -*- coding: utf-8 -*-

from datetime import date
import json


USER_DATA_PATH = '.cache/'


def get_calculated_vars(hsh):
    data = date.fromisoformat('2025-12-07')
    with open(USER_DATA_PATH + f'{hsh}/userdata.json', "r") as file:
        usr_data = json.load(file)
    return {
        "DATA": data,
        "TARGET_INVENTORY": usr_data['TARGET_INVENTORY'],
        "MAX_SAFE": usr_data['MAX_SAFE'],
        "START": usr_data['START'],
        "END": usr_data['END'],
        "MIN_SAFE": usr_data['MIN_SAFE']
    }

