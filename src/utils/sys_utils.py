from platform import system
from colorama import Style, Fore
from os import getenv
      
def get_user_path():
    if system() == "Windows":
        user = getenv("USERNAME")
        return f"C:\\Users\\{user}\\AppData\\Local\\Zap"
    elif system() == "Linux":
        user = getenv("USER")
        return f"/home/{user}/.zap/"
    elif system() == "MacOS":
        print(Style.BRIGHT + Fore.RED + "Say no to mac!")
        exit()
    else:
        print(Style.BRIGHT + Fore.RED + "Unsupported system!")
        exit()