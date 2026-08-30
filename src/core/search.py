from os import path, listdir
from platform import system

from src.core.confirm import confirm
from src.zap_path import PathManager
from src.utils.json_utils import read_json
from src.utils.write_logs import log_info, log_debug, log_warning

tmp_path = PathManager.get("tmp")
current_os = system()

# 1 - Receber indicações,
# 2 - procurar
# 3 - Ver dependencias
# 4 - Ver dependencias de dependencias
# 5 - Passar para o proximo
def search_repo_packages(packages, Number_of_process=0, skip_confirmation=False, search_dependencies=True):
    log_info("Searching for packages...")
    log_debug("Advanced information!")
    os_notsupported = []
    all_found_packages = []

    pending = set(packages)
    found = set()

    dependencies = []

    for file in listdir(tmp_path):
        if not pending:
            break

        if file.endswith(".json"):
            log_debug(f"Reading '{path.join(tmp_path, file)}'. ")
            data = read_json(path.join(tmp_path, file))
            base_url = data.get("base_url", "")

            for pkg in data.get("packages", []):

                pkg_name = pkg.get("name")
                log_debug(f"Package: {pkg_name}. ")

                if pkg_name in pending:
                    if pkg.get("system") == current_os:

                        pkg["repo"] = data.get("repo", "unknown")
                        pkg["url"] = base_url + pkg["url"]
                        pkg_dependencies = pkg.get("dependencies", False)

                        if pkg_dependencies is not False:
                            dependencies.extend(
                                x for x in pkg_dependencies
                                if x not in dependencies
                            )

                        log_debug("Found.")

                        all_found_packages.append(pkg)
                        found.add(pkg_name)

                        pending.remove(pkg_name)

                    else:
                        os_notsupported.append(pkg_name)
                        log_warning(f"Your os do not support '{pkg_name}'.")

    missingwf = set(packages) - found
    missing = missingwf - set(os_notsupported)

    if dependencies and search_dependencies == True:
        result = search_repo_packages(
            dependencies,
            Number_of_process=Number_of_process + 1
        )

        all_found_packages.extend(
            x for x in result["packages"]
            if x not in all_found_packages
        )

        missing = result["missing"]
        os_notsupported.extend(
            x for x in result["os_notsupported"]
            if x not in os_notsupported
        )

    if Number_of_process > 0:
        return {
            "packages": all_found_packages,
            "missing": list(missing),
            "os_notsupported": os_notsupported
        }
    
    if not all_found_packages:
        print("Package not found")
        log_warning("Package not found, exiting")
        exit(0)
    if skip_confirmation is True:
            return {
                "packages": all_found_packages,
                "missing": list(missing),
                "os_notsupported": os_notsupported
            }
    
    print("\nPackages to be installed:\n" if search_dependencies == True else "\nPackages to be downloaded:\n" )

    for pkg in all_found_packages:
        print(
            f"  {pkg['name']}"
            f"  {pkg.get('version', '')}"
            f"  [{pkg.get('repo', 'unknown')}]"
        )

    print(f"\nTotal: {len(all_found_packages)} packages")
    if skip_confirmation is False:
        if confirm() is False:
            exit(0)

    return {
        "packages": all_found_packages,
        "missing": list(missing),
        "os_notsupported": os_notsupported
    }