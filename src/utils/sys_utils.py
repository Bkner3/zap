from platform import system
from colorama import Style, Fore
from os import getenv

def what_system():
    if system() == "Windows":
        return "Windows"
    elif system() == "Linux":
        return "Linux"
    elif system() == "Darwin":
        return "MacOS"
    else:
        return "Not_supported"
    
    
def get_user_path():
    if what_system() == "Windows":
        user = getenv("USERNAME")
        return f"C:\\Users\\{user}\\AppData\\Local\\Zap"
    elif what_system() == "Linux":
        user = getenv("USER")
        return f"/home/{user}/.zap/"
    elif what_system() == "MacOS":
        print(Style.BRIGHT + Fore.RED + "Say no to mac!")
        exit()
    else:
        print(Style.BRIGHT + Fore.RED + "Unsupported system!")
        exit()