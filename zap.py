"""
Zippy Asset Packager - A simple package manager
#Version: 0.01 Alpha
Github: https://github.com/Bkner3/zap
This project is in early development, expect bugs and missing features.
"""
#3RD PARTY IMPORTS
import os
import sys
import shutil
from colorama import Fore, Back, Style, init
""""""
#ZAP STARTING PATH SYSTEM
from src.zap_path import PathManager

if getattr(sys, 'frozen', False):
    root = os.path.dirname(sys.executable)  # EXE or ELF
else:
    root = os.path.dirname(__file__) #Script
PathManager.setup(root)

#ZAP ESSENCIAL IMPORTS 
from src.core.add_repo import add_repo
from src.core.downloader import download_to
from src.core.config import config_zap
from src.core.install import install
from src.core.remove import remove
from src.core.list import list_packages
from src.utils.write_logs import setup_logger, log_info, log_warning, log_error, log_debug
from src.utils.sys_utils import what_system, get_user_path
from src.cli.parser import read_args
from src.cli.ui import show_on_start, show_help

init(autoreset=True)

user_path = get_user_path()

### Global Variables
version = "0.01"
tversion = "Alpha"
corversion = f"{version} {tversion} {what_system()} Edition"

current_dir = os.getcwd()
tmp_path = PathManager.get("tmp")

if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

command, packages = read_args()

show_on_start()
print(Style.BRIGHT + Fore.GREEN + f"Zippy Asset Packager - {corversion}")
print(Fore.CYAN + "──────────────────────────────────────────\n")

### Main_funcs

#commands
if command == "install":
    install(packages)
elif command == "remove":
    remove(packages)
elif command == "download":
    download_to(packages, current_dir)
elif command == "update":
    pass
elif command == "add":
    add_repo(packages)
elif command == "list":
    list_packages()
elif command =="help":
    show_help()
elif command == "config":
    config_zap(packages[0])
else:
    print("Use: zap help")