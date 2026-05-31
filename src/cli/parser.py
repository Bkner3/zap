import argparse
from sys import argv

from src.core.add_repo import add_repo
from src.core.downloader import download_to
from src.core.config import config_zap
from src.core.install import install
from src.core.remove import remove
from src.core.list import list_packages
from src.db.database import reset_db
from src.core.open_tools import open_tools

from src.cli.ui import show_on_start, show_help


def read_args():
    if len(argv) < 2:
        print("Use: zap <command> <package>")
        exit()

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
    command, packages = read_args()

    commands = {
        "install": lambda: install(packages),
        "remove": lambda: remove(packages),
        "download": lambda: download_to(packages, current_dir),
        "add": lambda: add_repo(packages),
        "list": list_packages,
        "help": show_help,
        "config": lambda: config_zap(packages[0]),
        "update": lambda: print("Update not implemented yet"),
        "reset-db": lambda:reset_db(),
        "version": lambda: """The show_on_start function already shows the version, so we don't need to do anything here. print("") just to avoid syntax error""",
        "open-tools": lambda: open_tools()
    }

    if command not in commands:
        print("Use: zap help")
        return

    show_on_start(corversion)
    commands[command]()