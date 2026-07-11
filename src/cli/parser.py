import argparse
from sys import argv, exit as sys_exit

from src.core.s_repo import add_repo, remove_repo
from src.core.downloader import download_to
from src.core.config import config_zap
from src.core.install import install
from src.core.remove import remove
from src.core.list import list_packages
from src.db.database import reset_db
from src.core.repo_tools import repo_tools
from src.core.update import update, upgrade
from src.utils.write_logs import log_info, log_error

from src.cli.ui import show_on_start, show_help

repo_tools_disabled = True  # Set to True to disable repo_tools command

def read_args():
    log_info("Reading command line arguments.")
    if len(argv) < 2:
        print("Use: zap <command> <package>")
        log_error("No command provided.")
        sys_exit(1)

    parser = argparse.ArgumentParser(description="Zap package manager")

    parser.add_argument(
        "command",
        help="Execute a command"
    )

    parser.add_argument(
        "packages",
        nargs="*",
        help="Packages"
    )

    args = parser.parse_args()

    return args.command, args.packages


def start(current_dir, corversion):
    log_info("Starting the parser module.")
    command, packages = read_args()

    commands = {
        "install": lambda: install(packages, "package"),
        "remove": lambda: remove(packages),
        "download": lambda: download_to(packages, current_dir),
        "repo-add": lambda: add_repo(packages),
        "repo-remove": lambda: remove_repo(packages),
        "list": list_packages,
        "help": show_help,
        "config": lambda: config_zap(packages[0]),
        "update": lambda: update(),
        "upgrade": lambda: upgrade(corversion),
        "reset-db": lambda:reset_db(),
        "version": lambda: """The show_on_start function already shows the version, so we don't need to do anything here. print("") just to avoid syntax error""",
        "repo-tools": lambda: print("Repo Tools are currently unavailable. To test them, open the ZAP source code, go to `src/cli/parser.py` (line 17), and set `repo_tools_disabled` to `False`."if repo_tools_disabled else repo_tools()),
    }

    if command not in commands:
        print("Use: zap help")
        log_error("Invalid command provided.")
        return

    show_on_start(corversion)
    log_info(f"Executing {command} with packages or args: {packages}")
    commands[command]()
    sys_exit(0)