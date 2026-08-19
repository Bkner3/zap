import json
import os

from src.utils.json_utils import save_json, read_json
from colorama import Fore
from src.zap_path import PathManager
from os.path import exists
from os import remove
from src.utils.write_logs import log_info

def config_zap(packages=None):
    if packages == "default":
        if exists(PathManager.get("config_file")): 
            remove(PathManager.get("config_file"))

    

    config = read_config()
    for config_key in config:
        print(f"Key: {config_key}, Value: {config[config_key]}")
    

def read_config():
    default_config = {
        "show_logo": True,
        "use_user_logo": "False",
        "user_logo": None,
        "is_on_debug": False
    }

    config_file = PathManager.get("config_file")

    if not exists(config_file):
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)
        log_info("Created default config.json file.")
        
    config = read_json(config_file)
    log_info("Loaded configuration from config.json.")
    return config