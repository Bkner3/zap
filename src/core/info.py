from src.db.database import get_package

def info(packages):
    if not packages:
        print("No select packages!")
        return
    print("Package info:")
    for package in packages:
        information = get_package(package)
        print(", ".join(information))
        
