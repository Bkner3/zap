from os import listdir, makedirs, path, remove

from src.core.downloader import only_download
from src.utils.move_files import move_files
from src.utils.create_launcher import create_launcher
from src.utils.zip_utils import extract_zip
from src.utils.json_utils import read_json
from src.zap_path import PathManager
from src.db.database import save_package
from src.core.search import search_repo_packages
from colorama import Fore, init

init(autoreset=True)

def install(packages):
    if not packages:
        print("No packages specified. Use: zap install <package>\n")
        return
    result= only_download(packages)
    successful_packages = result.get("downloaded", [])
    failed_packages = result.get("failed", [])
    missing_packages = result.get("missing", [])

    if not successful_packages:
        print("No packages were downloaded successfully.")
        return
    else:
        index = search_repo_packages(successful_packages)

    print("\nDownload completed. Installing packages...")

    ext_path = PathManager.get("ext")
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")
    index_file = PathManager.get("tmp_packages")
    
    for package in index["packages"]:
        package_name = package["name"]
        package_version = package["version"]
        package_desc = package["description"]

        filename = f"{package_name}.zip"
        file_path = path.join(ext_path, filename)
        
        print(f"\nInstalling {Fore.LIGHTMAGENTA_EX}{package_name}{Fore.RESET}...")

        install_folder = path.join(bin_path, package_name)
        target_file = path.join(install_folder, filename)

        if not path.exists(install_folder):
            makedirs(install_folder, exist_ok=True)

        move_files(file_path, install_folder)

        extract_zip(target_file, install_folder)
        print(f"Extracted {package_name}.")

        remove(target_file)

        executable_path = path.join(install_folder, f"{package_name}.exe")
        create_launcher(package_name, executable_path, symlinks_path)

        print(f"Created launcher for {package_name}.")

        save_package(
            package_name,
            package_version,
            package_desc
        )
        print(f"Saved {package_name} to database.")
        print(f"Installed {package_name} successfully.")

    print(f"\n{Fore.GREEN}Installation process completed.\n{Fore.RESET}Successfully installed: {Fore.GREEN}{', '.join(successful_packages)}")
    if missing_packages:
        print(f"Packages not found: {Fore.RED}{', '.join(missing_packages)}")
    if failed_packages:
        print(f"Failed to install: {Fore.LIGHTRED_EX} {', '.join(failed_packages)}")
    else:
        print(f"All packages installed successfully.\n")