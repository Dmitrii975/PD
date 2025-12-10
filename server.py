import json
import requests
import pickle
import os


def server_delete_account(uid):
    url = 'http://147.45.108.69:1488/delete_account'
    headers = {"Userid": str(uid)}
    r = requests.delete(url, headers=headers)
    return r.json()['response'] == 'Success!'

def send_table_file(pth, uid, name, future):
    url = 'http://147.45.108.69:1488/add_table'
    file_field_name = 'table' 
    with open(pth, 'rb') as f:
        files = {file_field_name: f}
        headers = {"Userid": str(uid), "Storagename": name, "Storagefuture": json.dumps(future)}
        response = requests.post(url, files=files, headers=headers)
        rsp = response.json()
        print(rsp)
        if rsp['response'] == 'Success!':
            return rsp['table_id']
        else:
            return None

def update_table_file(uid, tid, future, pth):
    url = 'http://147.45.108.69:1488/update_table' 
    file_field_name = 'table' 
    with open(pth, 'rb') as f:
        files = {file_field_name: f}
        headers = {"Userid": str(uid), "Storageid": str(tid)}
        if future != None:
            headers['Future'] = json.dumps(future)
        response = requests.put(url, files=files, headers=headers)
        print(response.json())

def add_offer(uid, count, time):
    url = 'http://147.45.108.69:1488/add_offer'
    headers = {"UserId": str(uid), "Count": str(count), "Time": str(time)}
    r = requests.post(url, headers=headers)
    if r['response'] == 'Success!':
        return r['offer_id']
    else:
        return None
    
def get_user_params(uid):
    url = 'http://147.45.108.69:1488/get_account_data'
    headers = {"Userid": str(uid)}
    r = requests.get(url, headers=headers)
    print(r.json())
    if r.json()['response'] == 'Success!':
        return r.json()
    else:
        None

def set_user_params(uid, ti=None, mxs=None, mns=None, st=None, en=None):
    url = 'http://147.45.108.69:1488/account_params_edit'
    headers = {"Userid": str(uid)}
    if ti != None:
        headers["Targetinventory"] = str(ti)
    if mxs != None:
        headers["Maxsafe"] = str(mxs)
    if mns != None:
        headers["Minsafe"] = str(mns)
    if st != None:
        headers["Start"] = str(st)
    if en != None:
        headers["End"] = str(en)
    r = requests.put(url, headers=headers)
    print(r.json())

import os
import pickle
import json
import requests

def read_warehouses_list(uid, hsh):
    url = 'http://147.45.108.69:1488/get_tables_data'
    headers = {"Userid": str(uid)}
    r = requests.get(url, headers=headers)
    
    # Добавьте проверку статуса!
    r.raise_for_status()  # выбросит исключение, если ошибка HTTP
    
    res = r.json()['massive']
    ls = []
    for i in json.loads(res):
        warehouse_data = {
            "table_id": i[1], 
            "name": i[2],
            "file_path": f'.cache/{hsh}/tables/{i[1]}.csv',
            "future": json.loads(i[3])  # ← убедитесь, что i[3] — строка JSON
        }
        ls.append(warehouse_data)
    
    print('Collected:', ls)
    
    # ✅ Создаём папку, если её нет
    os.makedirs(f'.cache/{hsh}', exist_ok=True)
    
    # Сохраняем
    with open(f'.cache/{hsh}/warehouses.pickle', 'wb') as f:
        pickle.dump(ls, f)
    
    return True  # ✅ вне блока with

def get_missed_tables(whs):
    print(whs)
    for i in whs:
        print(i['file_path'])
        if not os.path.exists(i['file_path']):
            url = 'http://147.45.108.69:1488/get_table_file_by_id'
            headers = {"Storageid": str(i['table_id'])}
            r = requests.get(url, headers=headers)
            print(r.status_code)
            with open(i['file_path'], "wb") as f:
                f.write(r.content)