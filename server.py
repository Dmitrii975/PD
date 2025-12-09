import requests

def server_delete_account(uid):
    url = 'http://147.45.108.69:5000/delete_account'
    headers = {"user_id": uid}
    r = requests.delete(url, headers=headers)
    return r['response'] == 'Success!'