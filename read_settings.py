import json

def read_settings():
    with open("./settings.json", 'r') as file:
        data = json.load(file)
    return data
