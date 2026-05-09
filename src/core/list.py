
from os import listdir
from src.zap_path import PathManager

def list_packages():
    packages = listdir(PathManager.get("bin"))
    if not packages:
        print("No packages installed.")
    print("Package list:")
    for package in packages:
        print(package)