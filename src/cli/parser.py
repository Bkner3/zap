import argparse
from sys import argv, exit as sys_exit

from src.core.s_repo import add_repo, remove_repo
from src.core.downloader import download_to
from src.core.config import config_zap
from src.core.install import install
from src.core.remove import remove
from src.core.list import list_packages
from src.db.database import reset_db
from src.repo_tools.repo_tools import repo_tools
from src.core.update import update, upgrade
from src.utils.write_logs import log_info, log_error
from src.core.info import info

from src.cli.ui import show_on_start, show_help

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
        "install": lambda: install(packages),
        "remove": lambda: remove(packages),
        "download": lambda: download_to(packages, current_dir),
        "repo-add": lambda: add_repo(packages),
        "repo-remove": lambda: remove_repo(packages),
        "list": list_packages,
        "help": show_help,
        "info": lambda: info(packages),
        "config": lambda: config_zap(packages[0]) if packages else print("Error: No package provided for config."),
        "update": lambda: update(),
        "upgrade": lambda: upgrade(corversion),
        "reset-db": lambda: reset_db(),
        "version": lambda: print(""),
        "repo-tools": lambda: print("Repo Tools are currently unavailable."),
    }

    if command not in commands:
        print("Use: zap help")
        log_error("Invalid command provided.")
        return

    show_on_start(corversion)
    log_info(f"Executing {command} with packages or args: {packages}")
    commands[command]()
    sys_exit(0)