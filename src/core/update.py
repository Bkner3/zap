import os
import sys
import subprocess
from platform import system
from colorama import Fore, Style

from src.db.database import get_all_packages
from src.core.downloader import download_index, get_context, download
from src.core.search import search_repo_packages
from src.core.install import install 
from src.utils.write_logs import log_info, log_warning, log_debug, log_error

def version_tuple(version):
    return tuple(map(int, version.split(".")))

def update():
    log_info("Update:")
    print(Fore.BLUE + Style.BRIGHT + "\nUpdate\n")
    packages_local = []
    packages_local_raw = get_all_packages()

    if not packages_local_raw:
        log_warning("No packages installed. No update needed.")
        print("No packages installed. No update needed.")
        return

    download_index(get_context())

    for package_itens in packages_local_raw:
        packages_local.append(package_itens[0])

    packages_list_on_repo = search_repo_packages(packages_local)["packages"]

    packages_to_update = []
    log_info("Verifying the versions of each package")
    print(Fore.BLUE + "\nVerifying the versions of each package\n")

    for package_local in packages_local_raw:
        package_name_local = package_local[0]
        version_local = package_local[1]
        log_debug(f"Name: {package_name_local}, Version: {version_local}")

        for package_repo in packages_list_on_repo:

            if package_repo["name"] != package_name_local:
                continue

            if version_tuple(version_local) < version_tuple(package_repo["version"]):
                log_info(
                    f"Update available for {package_name_local}: "
                    f"{version_local} -> {package_repo['version']}"
                )
                packages_to_update.append(package_repo["name"])
            else:
                log_debug(f"No need to upgrade to {package_name_local}.")

            break

    if not packages_to_update:
        print(Fore.GREEN + "All packages are up to date.")
        return

    print(Fore.BLUE + Style.BRIGHT + "Starting to download and install:\n")
    install(packages_to_update, "update")

def upgrade(current_version):
    #Make the condicion above false to test
    if 1==1:
        if not getattr(sys, 'frozen', False):
            print("The upgrade function is only avaiable for compiled zap")
            return
    url_api = "https://api.github.com/repos/Bkner3/zap/releases"
    cfg = get_context()

    log_info("Checking for the latest version available")
    print(Fore.BLUE + Style.BRIGHT + "Checking for the latest version available")
    json_name = "zap_latest.json"
    releases = download(url_api, json_name, "Index", cfg)
    
    if not releases or not isinstance(releases, list):
        log_error("GitHub couldn't check for updates.")
        print(Fore.RED + "GitHub couldn't check for updates.")
        return
    print(Fore.BLUE + Style.BRIGHT + "Download successful")

    last_release = releases[0]
    github_version = last_release["tag_name"]

    path_to_json = os.path.join(cfg["download"], json_name)
    if os.path.exists(path_to_json):
        os.remove(path_to_json)

    if github_version.lstrip('v').strip().lower() == current_version.lstrip('v').strip().lower():
        print(Fore.GREEN + f"ZAP is already up to date ({current_version}).")
        return
    
    print(Fore.GREEN + f"New version found: {github_version}!")
    
    # CORREÇÃO: Usar o system_os (que já está a ser importado corretamente da biblioteca platform)
    system_os = system().lower()
    target_asset = "zap.exe" if system_os == "windows" else "zap-linux"
    
    url_exe = None
    for asset in last_release["assets"]:
        if asset["name"] == target_asset:
            url_exe = asset["browser_download_url"]
            break
            
    if not url_exe:
        log_error(f"Executable asset ({target_asset}) not found in the latest release.")
        print(Fore.RED + f"Executable asset ({target_asset}) not found in the latest release.")
        return

    print(Fore.CYAN + "Downloading the new version...")
    temp_name = "zap_new.exe" if system_os == "windows" else "zap_new"
    new_exe_path = download(url_exe, temp_name, "Index", cfg)
    
    if new_exe_path and os.path.exists(new_exe_path):
        apply_update_and_restart(new_exe_path)
    else:
        log_error("Download failed. Update aborted.")
        print(Fore.RED + "Download failed. Update aborted.")

def apply_update_and_restart(new_exe_path):
    current_exe_path = os.path.abspath(sys.argv[0])
    current_dir = os.path.dirname(current_exe_path)
    binary_name = os.path.basename(current_exe_path)
    
    system_os = system().lower()
    
    if system_os == "windows":
        updater_script = os.path.join(current_dir, "update_updater.bat")
        bat_content = f"""@echo off
:loop
tasklist | findstr /i "{binary_name}" >nul
if %errorlevel% equ 0 (
    timeout /t 1 /nobreak >nul
    goto loop
)
del "{current_exe_path}"
move "{os.path.abspath(new_exe_path)}" "{current_exe_path}"
start "" "{current_exe_path}"
del "%~f0"
"""
        with open(updater_script, "w", encoding="utf-8") as f:
            f.write(bat_content)
            
        subprocess.Popen([updater_script], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    elif system_os == "linux":
        updater_script = os.path.join(current_dir, "update_updater.sh")
        sh_content = f"""#!/bin/bash
while kill -0 {os.getpid()} 2>/dev/null; do
    sleep 1
done
rm -f "{current_exe_path}"
mv "{os.path.abspath(new_exe_path)}" "{current_exe_path}"
chmod +x "{current_exe_path}"
"{current_exe_path}" &
rm -- "$0"
"""
        with open(updater_script, "w", encoding="utf-8") as f:
            f.write(sh_content)
            
        os.chmod(updater_script, 0o755)
        subprocess.Popen(["/bin/bash", updater_script], start_new_session=True)

    log_info("Launching external updater script and exiting ZAP.")
    print(Fore.YELLOW + "\nApplying updates... The application will restart automatically.")
    sys.exit(0)