import argparse
from sys import argv

def read_args():
    if len(argv) < 2:
        print("Use: zap <command> <package>")
        exit()
    parser = argparse.ArgumentParser(description="Zap package manager")
    parser.add_argument("command", help="Execute a command (install, remove, download, update, add, list, help)")
    parser.add_argument("packages", nargs="*", help="List of packages for the command")

    args = parser.parse_args()
    command = args.command
    packages = args.packages
    valid_commands = ["install", "remove", "download", "update", "update-all", "info", "add", "list", "help", "config", "search"]
    if command not in valid_commands:
        print(f"\nUse: zap help")
        exit()
    return command, packages

