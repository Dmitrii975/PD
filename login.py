import os

def login(email, password):
    hsh = hash(email + password)
    if os.path.exists(f'.cache/{hsh}/'):
        pass
