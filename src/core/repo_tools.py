from src.utils.json_utils import *
import os
from datetime import date
from src.zap_path import PathManager
from colorama import Fore, Style
from time import sleep
import hashlib

root = PathManager.get("root")

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest().upper()

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


def add_package(index_file):
    print(Fore.BLUE + Style.BRIGHT + "Add Package\n" + Style.RESET_ALL)

    name = input("Name: ").strip()
    version = input("Version: ").strip()
    description = input("Description: ").strip()
    file = input("File: ").strip()
    system = input("System: ").strip().lower()

    if os.path.exists(file):
        hash = calculate_hash(file)
    else:
        print(f"The file {file} doesn't exist")
        return
    
    url = None

    package = {
        "name": name,
        "version": version,
        "description": description,
        "url": url,
        "system": system,
        "hash": hash
    }

    data = read_json(index_file)
    data["packages"].append(package)
    create_json(index_file, data)

    print("Package added successfully.")


def edit_package():
    pass


def remove_package():
    pass


def repo_tools():
    found = False
    index_file = None

    sleep(1)

    while True:
        os.system("cls" if os.name == "nt" else "clear")

        if not found:
            print(Fore.BLUE + Style.BRIGHT + "Repo-tools\n" + Style.RESET_ALL)

            print(
                "[1] Create index\n"
                "[2] Select a index\n"
                "[3] Exit"
            )

            opt = input("> ").strip()

            if opt == "3":
                break
            elif opt == "1":
                index_file, found = create_index()
            elif opt == "2":
                index_file, found = select_index()

            continue

        print(Fore.BLUE + Style.BRIGHT + "Edit-repo" + Style.RESET_ALL)
        print(Fore.MAGENTA + f"Index: {index_file}\n" + Style.RESET_ALL)

        print(
            "[1] Add package\n"
            "[2] Edit a package\n"
            "[3] Remove a package\n"
            "[4] Go back\n"
            "[5] Exit"
        )

        opt = input("> ").strip()

        if opt == "5":
            break
        elif opt == "4":
            found = False
            index_file = None
        elif opt == "1":
            add_package(index_file)
        elif opt == "2":
            edit_package()
        elif opt == "3":
            remove_package()