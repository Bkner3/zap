import json

def save_json(key, value, file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    
    data[key] = value
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)