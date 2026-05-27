
from os import listdir
from src.db.database import get_all_packages

def list_packages():
    packages = get_all_packages()
    if not packages:
        print("No packages installed.")
    else:
        print("Package list:")
    for package in packages:
        print(package)