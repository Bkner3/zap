from platform import system as get_system
from src.zap_path import PathManager
from os import path
from shutil import rmtree
from src.db.database import init_db, delete_package
# Importe a função de onde você salvou o gerenciador de lançadores
from src.utils.launcher import remove_launcher 

def remove(packages):
    if not packages:
        print("No packages specified. Use: zap remove <package>\n")
        return
        
    bin_path = PathManager.get("bin")
    symlinks_path = PathManager.get("sl")
    system = get_system()
    init_db()
    
    for package in packages:
        package_path = path.join(bin_path, package)

        if not path.exists(package_path):
            print(f"Package not found: {package}")
            continue

        # 1. Deleta a pasta principal do pacote
        rmtree(package_path)

        # 2. Chama a função externa para isolar a limpeza do atalho
        remove_launcher(package, symlinks_path, system)
        
        # 3. Remove o registro do banco de dados
        delete_package(package)
        print(f"Removed package: {package}")