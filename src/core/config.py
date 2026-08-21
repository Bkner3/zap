import json
import os

from src.utils.json_utils import save_json, read_json, create_json
from colorama import Fore
from src.zap_path import PathManager
from os.path import exists
from os import remove
from src.utils.write_logs import log_info

config_file = PathManager.get("config_file")

def config_zap(packages=None):
    config = read_config()
    command = packages[0] #Commands to the config
    parameter = packages[1:] if packages is not None else None


    if command == "default":
        if exists(PathManager.get("config_file")): 
            remove(PathManager.get("config_file"))
    elif command == "list" or command is None:
        for config_key in config:
            print(f"Key: {config_key}, Value: {config[config_key]}")
    elif command == "set":

        if parameter[0] in config:
            value = parameter[1].lower()

            if value == "true":
                value = True
            elif value == "false":
                value = False
            else:
                value = " ".join(parameter[1:]).replace("\\n", "\n")
            save_json(parameter[0], value, config_file)
        else:
            print(
                f"Error: Configuration parameter '{parameter[0]}' not found."
                if parameter is not None
                else "Error: No parameter specified. Use 'zap config list' to view available parameters."
            )

def read_config():
    default_config = {
        "show_logo": True,
        "use_user_logo": False,
        "user_logo": None,
        "is_on_debug": False
    }

    if not exists(config_file):
        create_json(config_file, default_config)
        log_info("Created default config.json file.")
        
    config = read_json(config_file)
    log_info("Loaded configuration from config.json.")
    return config