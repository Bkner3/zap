from os import path, listdir
from platform import system

from src.zap_path import PathManager
from src.utils.json_utils import read_json

tmp_path = PathManager.get("tmp")
current_os = system()

def search_repo_packages(packages):

    os_notsupported = []
    all_found_packages = []
    
    pending = set(packages)
    found = set()

    dependencies = []

    for file in listdir(tmp_path):
        if not pending:
            break

        if file.endswith(".json"):
            data = read_json(path.join(tmp_path, file))
            base_url = data.get("base_url", "")

            for pkg in data.get("packages", []):
                pkg_name = pkg.get("name")

                if pkg_name in pending:
                    if pkg.get("system") == current_os:
                        
                        pkg["repo"] = data.get("repo", "unknown")
                        pkg["url"] = base_url + pkg["url"]

                        dependencies.append(pkg["dependencies"])
                        
                        all_found_packages.append(pkg)
                        found.add(pkg_name)
                        
                        pending.remove(pkg_name)
                    else:
                        os_notsupported.append(pkg_name)

    missingwf = set(packages) - found
    missing = missingwf - set(os_notsupported)
    
    return {
        "packages": all_found_packages,
        "missing": list(missing),
        "os_notsupported": os_notsupported
    }



def search_cli(packages):
    found = []
    search_term = str(packages).lower()

    for file in listdir(tmp_path):
        if file.endswith(".json"):
            data = read_json(path.join(tmp_path, file))
            base_url = data.get("base_url", "").rstrip("/")
        
            for pkg in data.get("packages", []):
                pkg_name = pkg.get("name", "")
                
                # Procura se o termo pesquisado faz parte do nome do pacote (case-insensitive)
                if search_term in pkg_name.lower():
                    repo_url = f"{base_url}/{pkg_name}" if base_url else ""
                    
                    found.append({
                        "pacote": pkg,
                        "repositorio": repo_url
                    })

    # Imprime a lista diretamente na consola em vez de retornar
    print(found)