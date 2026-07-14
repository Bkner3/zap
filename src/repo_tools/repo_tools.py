from src.utils.json_utils import *
import os
from src.repo_tools.repo_tools_cli import repo_cli
from datetime import date
from src.zap_path import PathManager
from colorama import Fore, Style

root = PathManager.get("root")

def create_index():
    print(Fore.BLUE + Style.BRIGHT + "\nCreate a repository:" + Style.RESET_ALL)

    repo_name = input("Write the repository name: ").strip()
    repo_url = input("Write the repository BASE URL: ").strip()
    index_file = os.path.join(root, f"{repo_name}.json")

    today = date.today().isoformat()

    index_data = {
        "repo": repo_name,
        "updated": today,
        "base_url": repo_url,
        "packages": []
    }

    create_json(index_file, index_data)

    return index_file, True


def select_index():
    files_list = os.listdir(root)

    print(Fore.BLUE + Style.BRIGHT + "List of files:" + Style.RESET_ALL)

    for file in files_list:
        print(file)

    index_file_name = input("Insert the repo name: ").strip()
    index_file = os.path.join(root, index_file_name)

    if not os.path.exists(index_file):
        print(f"The index file '{index_file}' does not exist.")
        return None, False

    return index_file, True


def repo_tools():
    print(Fore.BLUE + Style.BRIGHT + "\nRepository Management Menu:")
    print("[1] Create a new repository index""\n[2] Select an existing repository index""\n[3] Exit")

    choice = input(">").strip()

    match choice:
        case "3":
            return
        case "1":
            index_file, success = create_index()
        case "2":
            index_file, success = select_index()
        case _:
            print("Invalid choice. Please select a valid option.")
    if success:
        repo_cli(index_file)
        