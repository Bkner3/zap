import json

from src.utils.json_utils import save_json, read_json
from colorama import Fore
from src.zap_path import PathManager
from os.path import exists
from src.utils.write_logs import log_info

def config_zap(packages):
    config_file = PathManager.get("config_file")

    action = None
    target = None

    for c in packages:
        if c == "h":
            action = "hide"
        if c == "s":
            action = "show"
        if c == "c":
            action = "change"
        if c == "o":
            action = "original"
        """if c == "t":
            action = "true"
        if c == "f":
            action = "false"#"""
        if c == "l":
            target = "logo"
        if c == "d":
            target = "debug"
    
        
        # adiciona mais targets aqui

        if action and target:
            apply_config(action, target, config_file)
            action = None
            target = None

def apply_config(action, target, config_file):
    if target == "logo":
        if action == "hide":
            print(Fore.YELLOW + "Logo: " + Fore.RED + "OFF")
            save_json("show_logo", False, config_file)
        elif action == "show":
            print(Fore.YELLOW + "Logo: " + Fore.GREEN + "ON")
            save_json("show_logo", True, config_file)
        elif action == "original":
            print(Fore.YELLOW + "Logo: " + Fore.GREEN + "ON (Original)")
            save_json("type_logo", "original", config_file)
        elif action == "change":
            new_logo = input("Enter new logo (use \\n for new lines): ")
            print(Fore.YELLOW + "Logo: " + Fore.GREEN + "Custom")
            save_json("type_logo", new_logo.replace("\\n", "\n"), config_file)
    if target == "debug":
        if action == "show":
            print(Fore.YELLOW + "Debug mode: " + Fore.GREEN + "ON")
            save_json("is_on_debug", True, config_file)
        elif action == "hide":
            print(Fore.YELLOW + "Debug mode: " + Fore.RED + "OFF")
            save_json("is_on_debug", False, config_file)

def read_config():
    default_config = {
        "show_logo": True,
        "type_logo": "original",
        "is_on_tools": False,
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