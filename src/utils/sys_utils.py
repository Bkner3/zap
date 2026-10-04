from platform import system
from sys import exit as sys_exit
from subprocess import run
from colorama import Style, Fore
import os
      
def get_user_path():
    if system() == "Windows":
        user = os.getenv("USERNAME")
        return f"C:\\Users\\{user}\\AppData\\Local\\Zap"
    elif system() == "Linux":
        user = os.getenv("USER")
        return f"/home/{user}/.zap/"
    elif system() == "Darwin":
        print(Style.BRIGHT + Fore.RED + "Say no to mac!")
        sys_exit()
    else:
        print(Style.BRIGHT + Fore.RED + "Unsupported system!")
        sys_exit()

def open_path(path):
    if system() == "Windows":
        os.startfile(path)

    elif system() == "Darwin":
        run(["open", path])

    elif system() == "Linux":
        run(["xdg-open", path])
