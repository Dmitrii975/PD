import os
import json


def register_user(email, password, company_name):
    hsh = hash(email + password)

    if os.path.exists(f'.cache/{hsh}'):
        pass
    else:
        base = {
            "user_id": 0,
            "user_hash": hsh,
            "tables_path": ".cache/tables/",
            "user_data_path": ".cache/userdata.json",
            "target_inventory": 50,
            "safe_min": 30,
            "action_on": 70
        }
        os.mkdir(f'.cache/{hsh}')
        with open(f'.cache/{hsh}/userdata.json', 'w') as f:
            json.dump(base, f)
    
