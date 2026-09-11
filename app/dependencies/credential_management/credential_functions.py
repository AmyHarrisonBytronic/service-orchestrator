import os
from flask import Flask

def get_key(key_name):
    ''''''
    key = os.environ.get(key_name)
    if key != None: return key
    raise ValueError("Error : key not found in enviroment")