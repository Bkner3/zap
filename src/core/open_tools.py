from src.core.config import read_config
from src.core.config import save_json
from src.zap_path import PathManager

def create_index():
    
    pass
def add_package():
    pass
def edit_package():
    pass
def remove_package():
    pass


def open_tools():
    config = read_config()
    if config.get("is_on_tools", True):
        while True:
            print("Open Tools Menu:\n [1] Create Index [2] Add package \n [3] Edit package \n [4] Remove Package\n [5] Exit")
            choice = int(input("Choose an option: "))
            case = {
                1: lambda: print("Creating index..."),
                2: lambda: print("Adding package..."),
                3: lambda: print("Editing package..."),
                4: lambda: print("Removing package..."),
                5: lambda: save_json("is_on_tools", False, PathManager.get("config_file")) and exit(),
            }
    else:
        save_json("is_on_tools", True, PathManager.get("config_file"))
        