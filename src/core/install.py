from os import makedirs, path, remove

from src.core.downloader import only_download
from src.utils.move_files import move_files
from src.utils.launcher import create_launcher
from src.utils.zip_utils import extract_zip
from src.zap_path import PathManager
from src.db.database import save_package
from src.core.search import search_repo_packages
from colorama import Fore, Style, init
from platform import system
from src.utils.write_logs import log_warning, log_info

init(autoreset=True)

def install(packages, process):
    if not packages:
        log_warning("No packages specified.")
        print("No packages specified. Use: zap install <package>\n")
        return
    
    result = only_download(packages, process)
    successful_packages = result.get("downloaded", [])
    failed_packages = result.get("failed", [])
    missing_packages = result.get("missing", [])
    not_supported = result.get("os_notsupported", [])

    if not successful_packages:
        log_warning("No packages were downloaded successfully.")
        print("No packages were downloaded successfully.")
        return
    
    log_info(f"Searching from {successful_packages} in the index list.")
    index = search_repo_packages(successful_packages)

    log_info("Download completed. Installing packages...")
    print("\nDownload completed. Installing packages...")

    ext_path = PathManager.get("ext")
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")
    
    for package in index["packages"]:
        package_name = package["name"]
        package_version = package["version"]
        package_desc = package["description"]

        log_info("Package name: {package_name}, Package version {package_version}")

        filename = f"{package_name}.zip"
        file_path = path.join(ext_path, filename)
        
        print(f"\nInstalling {Fore.LIGHTMAGENTA_EX}{package_name}{Fore.RESET}...")

        install_folder = path.join(bin_path, package_name)
        target_file = path.join(install_folder, filename)

        if not path.exists(install_folder):
            log_info(f"Creating the instalation folder of {package_name} in {install_folder}")
            makedirs(install_folder, exist_ok=True)

        log_info(f"Moving {file_path} to {install_folder}")
        move_files(file_path, install_folder)

        extract_zip(target_file, install_folder)
        log_info(f"Deleting {target_file}")
        remove(target_file)

        if system() == "Windows":
            executable_path = path.join(install_folder, f"{package_name}.exe")
        else:
            executable_path = path.join(install_folder, package_name)

        create_launcher(package_name, executable_path, symlinks_path)

        print(f"Created launcher for {package_name}.")

        save_package(
            package_name,
            package_version,
            package_desc
        )
        print(f"Saved {package_name} to database.")
        log_info(f"Installed {package_name} successfully.")
        print(f"Installed {package_name} successfully.")

    print(f"\n{Fore.GREEN}Installation process completed.\n{Fore.RESET}Successfully installed: {Fore.GREEN}{', '.join(successful_packages)}")
    if not_supported:
        print(f"Packages not supported for your os: {Style.BRIGHT}{Fore.LIGHTRED_EX}{', '.join(not_supported)} ")
    if missing_packages:
        print(f"Packages not found: {Style.BRIGHT}{Fore.LIGHTRED_EX}{', '.join(missing_packages)}")
    if failed_packages:
        print(f"Failed to install: {Style.BRIGHT}{Fore.LIGHTRED_EX} {', '.join(failed_packages)}")
    else:
        print(f"All packages installed successfully.\n")