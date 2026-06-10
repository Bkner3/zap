from src.db.database import get_all_packages
from src.core.downloader import download_index, get_context
from src.core.search import search_repo_packages


def update():
    packages_local = []
    packages_local_raw = get_all_packages()
    if not packages_local_raw:
        print("No packages installed. No update needed.")
        return
    download_index(get_context())
    for package_itens in packages_local_raw:
        packages_local.append(package_itens[0])
    print(packages_local)


    packages_list_of_info = search_repo_packages(packages_local)
    print(packages_list_of_info)
    