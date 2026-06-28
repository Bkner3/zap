from src.core.config import read_config
from colorama import Style, Fore, init
init(autoreset=True)

def show_on_start(corversion):
    logo = """
    ███████╗ █████╗ ██████╗
    ╚══███╔╝██╔══██╗██╔══██╗
      ███╔╝ ███████║██████╔╝
     ███╔╝  ██╔══██║██╔═══╝
    ███████╗██║  ██║██║
    ╚══════╝╚═╝  ╚═╝╚═╝ PM"""
    config = read_config()
    if config.get("show_logo", True):
            if config.get("type_logo", "original") == "original":
                print(f"{Style.BRIGHT} {logo}")
            else:
                print(f"{Style.BRIGHT} {config.get('type_logo')}")

    print(Style.BRIGHT + Fore.GREEN + f"Zippy Asset Packager - {corversion}")
    print(Fore.CYAN + "──────────────────────────────────────────")

def show_help():
    help_info = f"""    Usage:
        {Fore.MAGENTA}zap {Fore.GREEN}<command> {Fore.CYAN}<package> {Fore.YELLOW}[options]{Fore.RESET}

        Commands:        
            {Fore.GREEN}install{Fore.RESET}       Install a package
            {Fore.GREEN}remove{Fore.RESET}        Remove a package
            {Fore.GREEN}download{Fore.RESET}      Download a package without installing
            {Fore.GREEN}update{Fore.RESET}        Update a specific package
            {Fore.GREEN}upgrade{Fore.RESET}       Update zap to the last version
            {Fore.GREEN}add{Fore.RESET}           Add a new repository
            {Fore.GREEN}search{Fore.RESET}        Search for packages in the repository
            {Fore.GREEN}list{Fore.RESET}          List all installed packages
            {Fore.GREEN}info{Fore.RESET}          Show detailed information about a package
            {Fore.GREEN}help{Fore.RESET}          Show this help message
            {Fore.GREEN}config{Fore.RESET}        Configure zap settings"""
    print(help_info)