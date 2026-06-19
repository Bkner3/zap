from src.zap_path import PathManager
from colorama import Style, Fore
from json import load
from src.utils.json_utils import create_json, save_json
import os
from src.utils.write_logs import log_info

def add_repo(repositories):
    repo_file = PathManager.get("repos_file")

    print(Style.BRIGHT + Fore.BLUE + "Starting to add repositories")
    log_info("Starting to add repositories")

    # Create repos.json if it doesn't exist
    if not os.path.exists(repo_file):
        data = {"repos": []}
        create_json(repo_file, data)
        log_info("Created repos.json file.")

    # Load existing repositories
    with open(repo_file, 'r') as f:
        data = load(f)
        log_info("Loaded existing repositories from repos.json.")

    for url in repositories:
        if url not in data["repos"]:
            data["repos"].append(url)
            log_info(f"Added repository: {url}")
            print(f"Added repository: {Fore.MAGENTA}{url}")
        else:
            log_info(f"Repository already exists: {url}")
            print(Fore.YELLOW + f"Repository already exists: {url}")

    print("Writing changes to repos.json")
    log_info("Writing changes to repos.json")

    save_json("repos", data["repos"], repo_file)

    print(Fore.GREEN + "Done!")
    log_info("Finished adding repositories")