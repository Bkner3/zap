from os import path, listdir
from platform import system

from src.zap_path import PathManager
from src.utils.json_utils import read_json


def search_repo_packages(packages):
    tmp_path = PathManager.get("tmp")

    current_os = system()

    os_notsupported = []
    all_found_packages = []
    found = set()

    for file in listdir(tmp_path):
        if file.endswith(".json"):
            data = read_json(path.join(tmp_path, file))
            base_url = data.get("base_url")

            for pkg in data.get("packages", []):
                if pkg["name"] in packages:
                    if pkg["system"] == current_os:
                        pkg["repo"] = data.get("repo", "unknown")
                        pkg["url"] = base_url + pkg["url"]
                        all_found_packages.append(pkg)
                        found.add(pkg["name"])
                    else:
                        os_notsupported.append(pkg["name"])
                

    missingwf = set(packages) - found
    missing = missingwf - set(os_notsupported)

    return {
        "packages": all_found_packages,
        "missing": list(missing),
        "os_notsupported": os_notsupported
    }