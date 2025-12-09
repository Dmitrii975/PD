import os
import requests
import json


def login(email, password):

    url = 'http://147.45.108.69:5000/login'
    headers = {"login": email, "Password": password}
    r = requests.get(url, headers=headers)
    ans = r.json()
    # TODO: Проверить папку 
    if ans['response'] == 'Success!':
        return ans['user_id']
    else:
        return None