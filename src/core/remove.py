from platform import system as get_system
from src.zap_path import PathManager
from os import path
from shutil import rmtree
from src.db.database import init_db, delete_package, get_package
from colorama import Fore

from src.utils.launcher import find_latest_installed_version
from src.core.confirm import confirm
from src.utils.versions_utils import separate_name_from_version
from src.utils.launcher import remove_launcher, create_launcher
from src.utils.write_logs import log_info
from src.core.search import search_repo_packages

def remove(packages):
    if not packages:
        log_info("No packages specified. Use: zap remove <package>")
        print("No packages specified. Use: zap remove <package>\n")
        return
        
    bin_path = PathManager.get("bin")
    init_db()

    print(f"Remove: {packages}")
    if not confirm():
        print("Exiting")
        exit(0)
    
    for package in packages:
        package, version = separate_name_from_version(package)
        if version == False:
            print(f"Removing all versions of '{package}'")
            package_path = path.join(bin_path, package)
            version = None
        else:
            print(f"Removing '{package}' version '{version}' ")
            package_path = path.join(bin_path, package, version)

        if not path.exists(package_path):
            log_info(f"Package not found: {package}")
            print(f"Package not found: {package}")
            continue

        rmtree(package_path)

        remove_launcher(package)
        #This will launch on the next realese!
        """
        if version:
            latest_installed = find_latest_installed_version(package)
            name, version, author, description, dependencies = get_package(package, latest_installed)
            print(name,version,author,description,dependencies)
            data = {   
                    "name": name,
                    "version": version,
                    "author": author,
                    "system": system(),
                    "description": description,
                    "dependencies": dependencies
                    }
            print(f"{name}@{version}")
            create_launcher(data, index=(search_repo_packages(packages=f"{name}@={version}", search_on_db=True)["packages"]))"""
                
        delete_package(package, version)
        log_info(f"Removed package: {package}")
        print(f"Removed package: {Fore.MAGENTA + package}, version: '{version}'")