from platform import system as get_system
from src.zap_path import PathManager
from os import path
from shutil import rmtree
from src.db.database import init_db, delete_package
from colorama import Fore

from src.core.confirm import confirm
from src.utils.versions_utils import separate_name_from_version
from src.utils.launcher import remove_launcher 
from src.utils.write_logs import log_info

def remove(packages):
    if not packages:
        log_info("No packages specified. Use: zap remove <package>")
        print("No packages specified. Use: zap remove <package>\n")
        return
        
    bin_path = PathManager.get("bin")
    init_db()
    
    for package in packages:
        package, version = separate_name_from_version(package)
        if version == False:
            print(f"Remove all versions of '{package}'?")
            if confirm():
                package_path = path.join(bin_path, package)
                version = None
            else:
                exit(0)

        else:
            print(f"Remove '{package}' version '{version}' ?")
            if confirm():
                package_path = path.join(bin_path, package, version)
            else:
                exit(0)

        if not path.exists(package_path):
            log_info(f"Package not found: {package}")
            print(f"Package not found: {package}")
            continue

        rmtree(package_path)

        remove_launcher(package)
        
        delete_package(package, version)
        log_info(f"Removed package: {package}")
        print(f"Removed package: {Fore.MAGENTA + package}")