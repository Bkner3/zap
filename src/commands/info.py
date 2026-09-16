from src.db.database import get_package
from src.utils.launcher import separate_name_from_version

def info(packages):
    if not packages:
        print("No select packages!")
        return
    print("Package info:")
    for package in packages:
        name, version = separate_name_from_version(package)
        info = get_package(name, version)
        print(info)
        
