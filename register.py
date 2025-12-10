# -*- coding: utf-8 -*-

import os
import json
import requests
import hashlib



def register_user(email, password, company_name):
    b = {"TARGET_INVENTORY": 50.0, "MAX_SAFE": 70.0, "START": 7, "END": 42, "MIN_SAFE": 30.0}

    url = 'http://147.45.108.69:1488/register'
    headers = {"login": email, "Password": password, "Company": company_name}
    r = requests.post(url, headers=headers)
    ans = r.json()

    if ans['response'] == 'Success!':
        hsh = hashlib.md5(str(ans['user_id']).encode('utf-8')).hexdigest()
        os.makedirs(f'.cache/{hsh}', exist_ok=True)
        with open(f'.cache/{hsh}/userdata.json', 'w') as f:
            json.dump(b, f)
        return ans['user_id']
    else:
        return None
    