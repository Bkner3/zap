import json

def save_json(key, value, file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    
    data[key] = value
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

from os.path import exists

def read_json(file_to_read):
    if exists(file_to_read):
        with open(file_to_read, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}