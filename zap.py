# Copyright (c) 2026 Bernardo
# Licensed under the MIT License.

"""
Zippy Asset Packager - A simple package manager
#Version: 0.7.0-beta
Github: https://github.com/Bkner3/zap
This project is in early development, expect bugs and missing features.
"""

#3RD PARTY IMPORTS
import os
import sys
import shutil
from platform import system

#ZAP STARTING PATH SYSTEM
from src.zap_path import PathManager

if getattr(sys, 'frozen', False):
    root = os.path.dirname(sys.executable)  # EXE or ELF
else:
    root = os.path.dirname(__file__) #Script

PathManager.setup(root)
# Initialize the path manager with the root directory 
# If you do not initialize it, the program will crash and will not work properly.

#ZAP ESSENCIAL IMPORTS 
from src.utils.write_logs import log_info, log_debug
from src.cli.parser import start

#ZAP STARTING
corversion = "v0.7.0-beta"
current_dir = os.getcwd()
tmp_path = PathManager.get("tmp")

#First logs
log_info(f"Zap {corversion}")
log_info(f"Current directory: {current_dir}")
log_debug(f"App: {sys.executable} File: {__file__}")

#Check if tmp directory exists and is clean
log_info("Starting to check if tmp directory exists and is clean.")
if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

if __name__ == "__main__":
    if system() == "Linux":
        #ENDS THE LINUX EXECUTION BECAUSE THE FUNCTION TO CREATE LAUNCHERS ARE NOT ADEPT TO LINUX
        print("Zap\nThe Linux version cannot be used yet, it is still in development.\n")
        exit(0)
        
    if system() == "Windows" or system() == "Linux":
        start(current_dir, corversion)

    print(f"{system()} not supported!!!")
    exit(0)
