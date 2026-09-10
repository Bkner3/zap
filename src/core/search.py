from os import path, listdir
from platform import system

from src.core.confirm import confirm
from src.utils.versions_utils import compare_versions_symbols, separate_name_from_version
from src.core.verify_int import verify_dependencies
from src.zap_path import PathManager
from src.utils.json_utils import read_json
from src.utils.write_logs import log_info, log_debug, log_warning

tmp_path = PathManager.get("tmp")
current_os = system()

def search_repo_packages(packages, Number_of_process=0, skip_confirmation=False, search_dependencies=True):
    log_info("Searching for packages...")
    log_debug("Advanced information!")

    if Number_of_process == 0:
        original_packages = packages

    os_notsupported = []
    all_found_packages = []
    found = set()
    dependencies = []
    pending = {}

    for package in packages:
        pkg_name, pkg_version_needed = separate_name_from_version(package)
        pending[pkg_name] = pkg_version_needed

    for file in listdir(tmp_path):
        if not pending:
            break

        if not file.endswith(".json"):
            continue

        file_path = path.join(tmp_path, file)
        log_debug(f"Reading '{file_path}'.")
        data = read_json(file_path)
        base_url = data.get("base_url", "")

        for pkg in data.get("packages", []):

            if not pending:
                break

            pkg_name = pkg.get("name")

            if not pkg_name:
                continue

            if pkg_name not in pending:
                continue

            version_needed = pending.get(pkg_name)

            log_debug(f"Package: {pkg_name}.")

            if pkg.get("system") != current_os:

                if pkg_name not in os_notsupported:
                    os_notsupported.append(pkg_name)

                log_warning(
                    f"Your os do not support '{pkg_name}'."
                )

                continue

            pkg_version = pkg.get("version", "0.0.0")

            if version_needed:

                if not compare_versions_symbols(
                    version_needed,
                    pkg_version
                ):
                    log_debug(
                        f"Version mismatch for '{pkg_name}': "
                        f"needed '{version_needed}', "
                        f"found '{pkg_version}'."
                    )

                    continue

            pkg["repo"] = data.get("repo", "unknown")
            pkg["url"] = base_url + pkg.get("url", "")

            log_debug(
                f"Found '{pkg_name}@{pkg_version}'."
            )

            all_found_packages.append(pkg)
            found.add(pkg_name)

            pending.pop(pkg_name)

            if search_dependencies:

                pkg_dependencies = pkg.get("dependencies", [])

                for dependency in pkg_dependencies:

                    if dependency not in dependencies:
                        dependencies.append(dependency)

    missing = set(pending.keys()) - found
    missing -= set(os_notsupported)

    if dependencies and search_dependencies:

        result = search_repo_packages(
            dependencies,
            Number_of_process=Number_of_process + 1,
            skip_confirmation=True,
            search_dependencies=True
        )

        for pkg in result["packages"]:

            if pkg not in all_found_packages:
                all_found_packages.append(pkg)

        for package in result["missing"]:

            if package not in missing:
                missing.add(package)

        for package in result["os_notsupported"]:

            if package not in os_notsupported:
                os_notsupported.append(package)

    if Number_of_process > 0:
        return {
            "packages": all_found_packages,
            "missing": list(missing),
            "os_notsupported": os_notsupported
        }
    blocked_packages = False
    
    if search_dependencies:
        all_found_packages, blocked_packages = verify_dependencies(all_found_packages, original_packages)

    if not all_found_packages:
        if blocked_packages:
            print("\nPackage blocked by dependencies not found:")

            for pkg in blocked_packages:
                print(f"  {pkg['name']} {pkg['version']}")
            exit(0)

        print("Package not found")

        log_warning(
            "Package not found, exiting"
        )

        exit(0)

    if skip_confirmation:
        return {
            "packages": all_found_packages,
            "missing": list(missing),
            "os_notsupported": os_notsupported,
            "blocked": blocked_packages
        }

    print(
        "\nPackages to be installed:\n"
        if search_dependencies
        else "\nPackages to be downloaded:\n"
    )

    for pkg in all_found_packages:
        print(
            f"  {pkg['name']}"
            f"  {pkg.get('version', '')}"
            f"  [{pkg.get('repo', 'unknown')}]"
        )

    print(
        f"\nTotal: {len(all_found_packages)} packages"
    )

    if blocked_packages:
        print("\nBlocked packages:")

        for pkg in blocked_packages:
            print(
                f"  {pkg['name']} {pkg['version']}"
            )

    if confirm() is False:
        exit(0)

    return {
        "packages": all_found_packages,
        "missing": list(missing),
        "os_notsupported": os_notsupported,
        "blocked": blocked_packages
    }