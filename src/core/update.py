from src.db.database import get_all_packages
from src.core.downloader import download_index, get_context
from src.core.search import search_repo_packages
from colorama import Fore, Style
from src.core.install import install 
from src.utils.write_logs import log_info, log_warning, log_debug

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

    