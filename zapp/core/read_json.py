import json
from os.path import exists

def read_json(file_to_read):
    if exists(file_to_read):
        with open(file_to_read, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}