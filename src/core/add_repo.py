from src.zap_path import PathManager
from colorama import Style, Fore
from json import load, dump
import os

def add_repo(repositories):
    repo_file = PathManager.get("repos_file")

    print(Style.BRIGHT + Fore.BLUE + "Starting to add repositories")

    if not os.path.exists(repo_file):
        data = {"repos": []}
        with open(repo_file, "w") as f:
            dump(data, f, indent=2)

    with open(repo_file, 'r') as f:
        data = load(f)

    for url in repositories:
        if url not in data["repos"]:
            data['repos'].append(url)
            print(f"Added repository: {Fore.MAGENTA}{url}")
        else:
            print(Fore.YELLOW + f"Repository already exists: {url}")

    print("Writing changes to repos.json")

    with open(repo_file, 'w') as f:
        dump(data, f, indent=2)

    print(Fore.GREEN + "Done!")
    