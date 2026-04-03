import os
import sys
import zipfile
import json
import tqdm
import shutil
import threading
import requests
import argparse
import time
from platform import system
from colorama import Fore, Back, Style, init
from urllib.parse import urlparse

from zapp.core.downloader import download
from zapp.core.save_json import save_json
from zapp.core.create_launcher import create_launcher
from zapp.core.save_packages_info import save_packages
from zapp.core.read_json import read_json
from zapp.core.move_files import move_files

init(autoreset=True)

if system() == "Windows":
    user = os.getenv("USERNAME")
    user_path = f"C:\\Users\\{user}\\AppData\\Local\\Zap"
elif system() == "Linux":
    user = os.getenv("USER")
    user_path_path = f"/home/{user}/.zap/"
elif system() == "Darwin":
    print(Style.BRIGHT + Fore.RED + "Say no to mac!")
    exit()
else:
    print(Fore.RED + "system not supported!")
    exit()

### Global Variables
version = "0.01"
tversion = "Alpha"
corversion = f"{version} {tversion} {system()} Edition"

if getattr(sys, 'frozen', False):
    root = os.path.dirname(sys.executable)  # EXE
else:
    root = os.path.dirname(__file__) 

bin_path = user_path + "/bin"
sl_path = user_path + "/sl"
user_data_path = user_path + "/data"
inst_path = user_path + "/inst"
config_path = user_data_path + "/zap"
data_path = root + "/zapp"
core_path = data_path + "/core"
download_path = data_path + "/down"
core_path = data_path + "/core"
ext_path = data_path + "/ext"
tmp_path = data_path + "/tmp"

config_file = config_path + "/config.json"
tmp_file = f"{tmp_path}/Packages.tmp"
tmp_json_file = f"{tmp_path}/Packages_tmp.json"
repo_file = data_path + "/repos.json"
current_dir = os.getcwd()

if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)
### Create folders
paths = [
    data_path,
    core_path,
    bin_path,
    user_data_path,
    download_path,
    ext_path,
    inst_path,
    tmp_path,
    sl_path,
    config_path
]

for path in paths:
    os.makedirs(path, exist_ok=True)

logo = """
███████╗ █████╗ ██████╗
╚══███╔╝██╔══██╗██╔══██╗
  ███╔╝ ███████║██████╔╝
 ███╔╝  ██╔══██║██╔═══╝
███████╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝ PM
"""

config = read_json(config_file)
repos = read_json(repo_file).get("repos")

### Read Args
if len(sys.argv) < 2:
        print("Use: zap <command> <package>")
        sys.exit(1)

parser = argparse.ArgumentParser(description="Zap package manager")
parser.add_argument("command", help="Execute a command (install, remove, download, update, add, list, help)")
parser.add_argument("packages", nargs="*", help="List of packages for the command")

args = parser.parse_args()

command = args.command
packages = args.packages

if config.get("show_logo", True):
    if config.get("type_logo", "original") == "original":
        print(f"{Style.BRIGHT} {logo}")
    else:
        print(f"{Style.BRIGHT} {config.get('type_logo')}")
else:
    print()

print(Style.BRIGHT + Fore.GREEN + f"Zippy Asset Packager - {corversion}")
print(Fore.CYAN + "──────────────────────────────────────────\n")

### Main_funcs
def search_repo_packages():
    tmp_file = f"{tmp_path}/Packages.tmp"

    # limpar ficheiros
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    if os.path.exists(tmp_json_file):
        os.remove(tmp_json_file)

    todos_encontrados = []

    print("Downloading packages:")

    for file in os.listdir(tmp_path):
        if file.endswith(".json"):
            data = read_json(os.path.join(tmp_path, file))

            for pkg in data.get("packages", []):
                if pkg["name"] in packages:
                    pkg["repo"] = data.get("repo", "unknown")
                    todos_encontrados.append(pkg)

                        # guardar também no tmp txt
                    with open(tmp_file, "a") as tmp:
                        tmp.write(f"{pkg['name']} - {pkg['url']}\n")

    # guardar JSON FINAL (uma vez só)
    resultado = {
        "packages": todos_encontrados
    }

    with open(tmp_json_file, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

def get_package_url(data, name):
    for pkg in data["packages"]:
        if pkg["name"] == name:
            return pkg["url"]
    return None

def file_extraction(file_to_extract):
    extract_dir = os.path.dirname(file_to_extract)
    with zipfile.ZipFile(file_to_extract, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def add_repo(packages):
    print(Style.BRIGHT + Fore.BLUE + "Starting to add repositories")
    with open(repo_file, 'r') as f:
        data = json.load(f)

    for url in packages:
        data['repos'].append(url)
        print(f"Added repository: {Fore.MAGENTA}{url}")

    print("Writing changes to repos.json")
    with open(repo_file, 'w') as f:
        json.dump(data, f, indent=2)
        print(Fore.GREEN + "Done!")

def remove():
    if system() == "Windows":
        for package in packages:
            package_path = os.path.join(bin_path, package)
            if os.path.exists(package_path):
                shutil.rmtree(package_path)
                bat_file = os.path.join(sl_path, f"{package}.bat")
                if os.path.exists(bat_file):
                    os.remove(bat_file)
                print(f"Removed package: {package}")
            else:
                print(f"Package not found: {package}")

    elif system() == "Linux":
        for package in packages:
            package_path = os.path.join(bin_path, package)
            if os.path.exists(package_path):
                shutil.rmtree(package_path)
                link = os.path.join(sl_path, package)
                if os.path.islink(link):
                    os.unlink(link)
                print(f"Removed package: {package}")
            else:
                print(f"Package not found: {package}")

def install():
    only_download()
    for file in os.listdir(ext_path):
        print(f"Installing {file}...")
        pfile = os.path.join(ext_path, file)
        name = os.path.splitext(file)[0]
        final_folder = os.path.join(bin_path, name)
        final_file = os.path.join(final_folder, file)
        if not os.path.exists(final_folder):
            os.makedirs(final_folder)

        move_files(pfile, final_folder)
        file_extraction(os.path.join(final_folder, final_file))
        os.remove(final_file)
        
        executable = os.path.join(final_folder, f"{name}.exe")
        create_launcher(name, executable, sl_path)

def only_download():
    download_index()
    print()
    search_repo_packages()

    threads = []
    if not os.path.exists(tmp_file):
        print(Fore.YELLOW + "No packages found to download.")
        return
    with open(tmp_file, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if '-' not in line:
            continue  # ignora linhas inválidas

        output_name, url = line.split('-', 1)  # divide só no primeiro '-'
        output_name = output_name.strip()
        url = url.strip()  # remove espaços extras
        if not os.path.splitext(output_name)[1]:
            ext = os.path.splitext(url)[1]  # pega a extensão do arquivo na URL
            output_name += ext
        type="Package"
        t = threading.Thread(target=download, args=(url, output_name, type, ext_path, download_path))
        t.start()
        threads.append(t)

    # Espera todas as threads terminarem
    for t in threads:
        t.join()

def download_index():
    print(Style.BRIGHT + Fore.BLUE + "Starting to download repositories index")
    print()
    time.sleep(1)
    for url in repos:
        name = url.replace("http://", "").replace("https://", "").rstrip("/")
        index_url = url.rstrip("/") + "/index.zip"
        print(f"Updating: {index_url}")

        temp_zip = download(url=index_url, output_name=f"{name}.zip", type="Index", ext_path=ext_path, download_path=download_path)
        if temp_zip is None:
            print(Fore.YELLOW + f"Repository {url} is not available, jumping to next one.")
            continue

        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(tmp_path)
        os.remove(temp_zip)
        with open(f"{tmp_path}/index.json", "r") as f:
            data = json.load(f)
        original = tmp_path + "/index.json"
        final = tmp_path + "/" + data["repo"] + ".json"
        if os.path.exists(final):
            os.remove(final)
        os.rename(original, final)

def config(commands):
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
            apply_config(action, target)
            action = None
            target = None

def apply_config(action, target):
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

#commands
if command == "install":
    install()
elif command == "remove":
    remove()
elif command == "download":
    only_download()
    for file in os.listdir(ext_path):
        shutil.move(os.path.join(ext_path, file), os.path.join(current_dir, file))
elif command == "update":
    pass
elif command == "add":
    add_repo(packages)
elif command == "list":
    packages = os.listdir(bin_path)
    if not packages:
        print("No packages installed.")
    print("Package list:")
    for package in packages:
        print(package)
elif command =="help":
    #Help_info
    help_info = f"""    Usage:
        {Fore.MAGENTA}zap {Fore.GREEN}<command> {Fore.CYAN}<package> {Fore.YELLOW}[options]{Fore.RESET}

    Commands:        
        {Fore.GREEN}install{Fore.RESET}       Install a package
        {Fore.GREEN}remove{Fore.RESET}        Remove a package
        {Fore.GREEN}download{Fore.RESET}      Download a package without installing
        {Fore.GREEN}update{Fore.RESET}        Update a specific package
        {Fore.GREEN}update-all{Fore.RESET}    Update all installed packages
        {Fore.GREEN}add{Fore.RESET}           Add a new repository
        {Fore.GREEN}search{Fore.RESET}        Search for packages in the repository
        {Fore.GREEN}list{Fore.RESET}          List all installed packages
        {Fore.GREEN}info{Fore.RESET}          Show detailed information about a package
        {Fore.GREEN}help{Fore.RESET}          Show this help message

    """
    print(help_info)
elif command == "config":
    config(args.packages[0])
else:
    print("Use: zap help")