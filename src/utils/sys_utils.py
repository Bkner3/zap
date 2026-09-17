from platform import system
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
        exit()
    else:
        print(Style.BRIGHT + Fore.RED + "Unsupported system!")
        exit()

def open_path(path):
    if system() == "Windows":
        os.startfile(path)

    elif system() == "Darwin":
        run(["open", path])

    elif system() == "Linux":
        run(["xdg-open", path])
