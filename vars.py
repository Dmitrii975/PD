from datetime import date
import json

USER_DATA_PATH = '.cache/'

def get_calculated_vars(userid):
    data = date.fromisoformat('2025-12-07')
    with open(USER_DATA_PATH + f'{hash(userid)}/userdata.json', "r") as file:
        usr_data = json.load(file)
    return {
        'DATA': data,
        'TARGET_INVENTORY': usr_data['target_inventory'],
        'ACTION_ON': usr_data['action_on']
    }

