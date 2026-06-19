
from src.db.database import get_all_packages
from src.utils.write_logs import log_info, log_warning

def list_packages():
    packages = get_all_packages()
    if not packages:
        log_warning("No packages installed.")
        print("No packages installed.")
    else:
        print("Package list:")
        log_info("Package list:")
        log_info(packages)
        for package in packages:
            print(", ".join(package))