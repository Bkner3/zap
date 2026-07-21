from colorama import Fore, Style, init as colorama_init
from readchar import readkey, key
import os
from platform import system as platform_system

colorama_init(autoreset=True)

def tui():
    option = 0

    while True:
        os.system("cls" if platform_system() == "Windows" else "clear")
        print(Fore.BLUE + Style.BRIGHT + "ZAP repository tools\n")

        print(
            f"{'> ' if option == 0 else '  '}Create Repository\n"
            f"{'> ' if option == 1 else '  '}Select Repository\n"
            f"{'> ' if option == 2 else '  '}Exit"
        )

        input_key = readkey()

        if input_key == key.UP:
            if option > 0:
                option -= 1

        elif input_key == key.DOWN:
            if option < 2:
                option += 1

        elif input_key == key.ENTER:
            match option:
                case 0:
                    print("Create Repository")
                case 1:
                    print("Select Repository")
                case 2:
                    print("Bye ;)")
                    exit()
                
            

tui()