from os import path, remove, listdir
from src.zap_path import PathManager
from src.utils.json_utils import read_json
from json import dump

tmp_packages_file = PathManager.get("tmp_packages")
tmp_path = PathManager.get("tmp")

def search_repo_packages(packages):

    if path.exists(tmp_packages_file):
        remove(tmp_packages_file)

    todos_encontrados = []

    print("Downloading packages:")

    for file in listdir(tmp_path):
        if file.endswith(".json"):
            data = read_json(path.join(tmp_path, file))

            for pkg in data.get("packages", []):
                if pkg["name"] in packages:
                    pkg["repo"] = data.get("repo", "unknown")
                    todos_encontrados.append(pkg)

    resultado = {
        "packages": todos_encontrados
    }

    with open(tmp_packages_file, "w", encoding="utf-8") as f:
        dump(resultado, f, indent=2, ensure_ascii=False)