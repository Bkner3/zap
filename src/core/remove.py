from platform import system as get_system
from src.zap_path import PathManager
from os import path
from shutil import rmtree
from src.db.database import init_db, delete_package
from colorama import Fore

from src.utils.launcher import remove_launcher 
from src.utils.write_logs import log_info

def remove(packages):
    if not packages:
        log_info("No packages specified. Use: zap remove <package>")
        print("No packages specified. Use: zap remove <package>\n")
        return
        
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")
    system = get_system()
    init_db()
    
    for package in packages:
        package_path = path.join(bin_path, package)

        if not path.exists(package_path):
            log_info(f"Package not found: {package}")
            print(f"Package not found: {package}")
            continue

        rmtree(package_path)

        remove_launcher(package, symlinks_path, system)
        
        delete_package(package)
        log_info(f"Removed package: {package}")
        print(f"Removed package: {Fore.MAGENTA + package}")