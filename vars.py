from datetime import date
import json

TABLES_PATH = '.cache/tables/'
USER_DATA_PATH = '.cache/userdata.json'
DATA = None
CUR_USER_ID = None

def get_calculated_vars():
    global DATA, CUR_USER_ID

    DATA = date.fromisoformat('2025-12-07')
    with open(USER_DATA_PATH, "r") as file:
        usr_data = json.load(file)
    CUR_USER_ID = usr_data['user_id']
