"""
MIT License

Copyright (c) 2026 Bernardo Miguel Fernandes Quaresma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
"""
Zippy Asset Packager - A simple package manager
#Version: 0.5.0-beta
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

corversion = "0.5.0-beta"
current_dir = os.getcwd()
tmp_path = PathManager.get("tmp")

if os.path.exists(tmp_path):
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

start(current_dir, corversion)