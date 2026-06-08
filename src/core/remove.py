from src.utils.sys_utils import what_system
from src.zap_path import PathManager
from os import path, unlink, remove as os_remove
from shutil import rmtree
from src.db.database import init_db, delete_package

def remove(packages):
    if not packages:
        print("No packages specified. Use: zap remove <package>\n")
        return
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")
    system = what_system()
    init_db()
    
    for package in packages:
        package_path = path.join(bin_path, package)

        if not path.exists(package_path):
            print(f"Package not found: {package}")
            continue

        rmtree(package_path)

        launcher_path = (
            path.join(symlinks_path, f"{package}.bat")
            if system == "Windows"
            else path.join(symlinks_path, package)
        )

        if system == "Windows":
            if path.exists(launcher_path):
                os_remove(launcher_path)

        elif system == "Linux":
            if path.islink(launcher_path):
                unlink(launcher_path)
        
        delete_package(package)
        print(f"Removed package: {package}")