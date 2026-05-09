from src.utils.json_utils import save_json, read_json
from colorama import Fore, Style
from src.cli.parser import read_args
from src.zap_path import PathManager


packages, commands = read_args()

def config_zap(commands):
    config_file = PathManager.get("config_file")
    action = None
    target = None

    for c in commands:
        if c == "h":
            action = "hide"
        elif c == "s":
            action = "show"
        elif c == "c":
            action = "change"
        elif c == "o":
            action = "original"
        elif c == "l":
            target = "logo"
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

def read_config(config_file):
    config = read_json(config_file)
    return config