from datetime import date
import json


USER_DATA_PATH = '.cache/userdata.json'

def get_calculated_vars():
    data = date.fromisoformat('2025-12-07')
    with open(USER_DATA_PATH, "r") as file:
        usr_data = json.load(file)
    return {
        'DATA': data,
        'USER_ID': usr_data['user_id'],
        'TABLES_PATH': usr_data['tables_path'],
        'TARGET_INVENTORY': usr_data['target_inventory'],
        'SAFE_MIN': usr_data['safe_min'],
        'ACTION_ON': usr_data['action_on']
    }

