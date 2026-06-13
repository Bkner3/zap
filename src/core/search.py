from os import path, listdir
from src.zap_path import PathManager
from src.utils.json_utils import read_json
from os import path, listdir

def search_repo_packages(packages):
    tmp_path = PathManager.get("tmp")

    all_found_packages = []
    found = set()

    for file in listdir(tmp_path):
        if file.endswith(".json"):
            data = read_json(path.join(tmp_path, file))

            for pkg in data.get("packages", []):
                if pkg["name"] in packages:
                    pkg["repo"] = data.get("repo", "unknown")
                    all_found_packages.append(pkg)
                    found.add(pkg["name"])

    missing = set(packages) - found

    return {"packages": all_found_packages, "missing": list(missing)}