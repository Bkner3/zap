from src.zap_path import PathManager
from colorama import Style, Fore
from json import load, dump

def add_repo(repositories):
    repo_file = PathManager.get("repos_file")
    print(Style.BRIGHT + Fore.BLUE + "Starting to add repositories")
    with open(repo_file, 'r') as f:
        data = load(f)

    for url in repositories:
        data['repos'].append(url)
        print(f"Added repository: {Fore.MAGENTA}{url}")

    print("Writing changes to repos.json")
    with open(repo_file, 'w') as f:
        dump(data, f, indent=2)
        print(Fore.GREEN + "Done!")