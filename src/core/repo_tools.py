from src.utils.json_utils import *
import os
from datetime import date
from src.zap_path import PathManager
from colorama import Fore, Style

root = PathManager.get("root")

def create_index():
    print(Fore.BLUE + Style.BRIGHT +  "\nCreate a repository:" + Style.RESET_ALL)
    repo_name = input("Write the repository name:")
    repo_file = os.path.join(root, repo_name, ".json")
    today = date.today().isoformat()

    repo_data = {
        "repo": repo_name,
        "updated": today,
        "packages": []
    } 
    create_json(repo_file, repo_data)

def select_index():
    files_list = os.listdir(root)
    print(Fore.BLUE + "List of files:")
    for file in files_list:
        print("" + file)
    repo_name = input("Insert the repo name:")
     
def add_package():
    pass
def edit_package():
    pass
def remove_package():
    pass


def repo_tools():
    while True:
        print("repo-tools")
        print(
            "[1] Create index\n"\
            "[2] Select a index\n"\
            "[3] Exit"
        )
        opt = input(">") 
        if opt == "3":
            break
        if opt == "1":
            create_index()
        if opt == "2":
            select_index()