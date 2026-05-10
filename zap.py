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

#ZAP STARTING PATH SYSTEM
from src.zap_path import PathManager

if getattr(sys, 'frozen', False):
    root = os.path.dirname(sys.executable)  # EXE or ELF
else:
    root = os.path.dirname(__file__) #Script
PathManager.setup(root)

#ZAP ESSENCIAL IMPORTS 
from src.utils.write_logs import setup_logger, log_info, log_warning, log_error, log_debug
from src.cli.parser import start

corversion = "0.01 Alpha"
current_dir = os.getcwd()
tmp_path = PathManager.get("tmp")

if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

start(current_dir)