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

init(autoreset=True)

if system() == "Windows":
    user = os.getenv("USERNAME")
    user_path = f"C:\\Users\\{user}\\AppData\\Local\\Zap"
elif system() == "Linux":
    user = os.getenv("USER")
    user_path_path = f"/home/{user}/.zap/"
elif system() == "Darwin":
    print("Say no to mac!")
    exit()
else:
    print(Fore.RED + "system not supported!")
    exit()

### Global Variables
data_path = "zapp"
core_path = data_path + "/core"
bin_path = user_path + "/bin"
user_data_path = user_path + "/data"
download_path = data_path + "/down"
ext_path = data_path + "/ext"
tmp_path = data_path + "/tmp"
tmp_file = f"{tmp_path}/Packages.tmp"

### Create folders
paths = [
    data_path,
    core_path,
    bin_path,
    user_data_path,
    download_path,
    ext_path,
    tmp_path
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

def read_json():
    config_file = data_path + "/repos.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

### Read repos.json
repos = read_json().get("repos")

### Read Args
if len(sys.argv) < 2:
        print("Use: zap <command> <package>")
        sys.exit(1)

parser = argparse.ArgumentParser(description="Zap package manager")
parser.add_argument("command", help="Comando a executar (install, update, etc.)")
parser.add_argument("packages", nargs="*", help="Lista de pacotes para o comando")

args = parser.parse_args()

command = args.command
packages = args.packages

print(Style.BRIGHT + " " + logo)

### Main_funcs
def search_repo_packages():
    tmp_file = f"{tmp_path}/Packages.tmp"
    #clear the tmp_file before used
    if os.path.exists(tmp_file):
        os.remove(tmp_file)

    for file in os.listdir(tmp_path):
        if file.endswith(".json"):
            with open(os.path.join(tmp_path, file), "r") as f:
                data = json.load(f)
                print("Downloading packages:")
                for package in packages:
                    url = get_package_url(data, package)

                    if url:
                        with open(tmp_file, "a") as tmp:
                            tmp.write(f"{package} - {url}\n")

def get_package_url(data, name):
    for pkg in data["packages"]:
        if pkg["name"] == name:
            return pkg["url"]
    return None

def install():
    only_download()

def only_download():
    download_index()
    print()
    search_repo_packages()

    threads = []

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

        t = threading.Thread(target=download, args=(url, output_name))
        t.start()
        threads.append(t)

    # Espera todas as threads terminarem
    for t in threads:
        t.join()

def download_index():
    time.sleep(1)
    for url in repos:
        name = url.replace("http://", "").replace("https://", "").rstrip("/")
        index_url = url.rstrip("/") + "/index.zip"
        print(f"Updating: {index_url}")
        temp_zip = download(url=index_url, output_name=f"{name}.zip")

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

def download(url, output_name):
    output = f"{download_path}/{output_name}"

    r = requests.get(url, stream=True)
    r.raise_for_status()
    total = int(r.headers.get("content-length", 0))

    with open(output, "wb") as f, tqdm.tqdm(total=total if total > 0 else None, unit="B", unit_scale=True, desc=output_name) as bar:
        for chunk in r.iter_content(8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))

    return output

def remove():
    pass
#commands
if command == "install":
    install()
elif command == "remove":
    remove()
elif command == "download":
    only_download()
elif command == "update":
    pass
elif command == "add":
    repo = read_json().get("repos")
elif command =="help":
    #Help_info
    help_info = """Zippy Asset Packager (Zap)

    Usage:
        zap <command> <package> [options]

    Commands:        
        install       Install a package
        remove        Remove a package
        download      Download a package without installing
        update        Update a specific package
        update-all    Update all installed packages
        search        Search for packages in the repository
        list          List all installed packages
        info          Show detailed information about a package
        help          Show this help message

    """
    print(help_info)
else:
    print("Use: zap help")