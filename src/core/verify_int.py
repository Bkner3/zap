from src.utils.versions_utils import compare_versions_symbols, separate_name_from_version
from colorama import Fore

def verify_dependencies(packages_found_list, original_packages, Number_of_process=0, checked_packages=None, packages_to_check=None):
    if Number_of_process == 0:
        print("\nChecking if all packages are found...\n")
    if checked_packages is None:
        checked_packages = {}

    if packages_to_check is None:
        packages_to_check = []

        for original_package in original_packages:
            name, version_needed = separate_name_from_version(original_package)

            for package in packages_found_list:
                if package["name"] != name:
                    continue

                if version_needed:
                    if not compare_versions_symbols(version_needed, package["version"]):
                        continue

                packages_to_check.append(package)
                break

    blocked_packages = []

    for package in packages_to_check:
        package_name = package["name"]
        package_version = package["version"]

        package_id = (package_name, package_version)

        if package_id in checked_packages:
            if checked_packages[package_id] is False:
                blocked_packages.append(package)

            continue

        checked_packages[package_id] = True

        package_valid = True

        for dependency in package.get("dependencies", []):
            dependency_name, dependency_version = separate_name_from_version(dependency)

            dependency_package = None

            for candidate in packages_found_list:
                if candidate["name"] != dependency_name:
                    continue

                if dependency_version:
                    if not compare_versions_symbols(dependency_version,candidate["version"]):
                        continue

                dependency_package = candidate
                break

            if dependency_package is None:
                #print(f"Dependency '{dependency}' not found "f"for '{package_name}@{package_version}'.")

                package_valid = False
                break

            _, dependency_blocked = verify_dependencies(
                packages_found_list,
                original_packages,
                Number_of_process + 1,
                checked_packages,
                [dependency_package]
            )

            if dependency_blocked:
                package_valid = False
                break

        checked_packages[package_id] = package_valid

        if not package_valid:
            blocked_packages.append(package)

    if Number_of_process == 0:
        blocked_ids = {(package["name"], package["version"])for package in blocked_packages}

        original_ids = set()

        for original_package in original_packages:
            name, version_needed = separate_name_from_version(original_package)

            for package in packages_found_list:
                if package["name"] != name:
                    continue

                if version_needed:
                    if not compare_versions_symbols(version_needed,package["version"]):
                        continue

                original_ids.add((package["name"], package["version"]))
                break

        final_packages = []

        def add_package(package):
            package_id = (package["name"],package["version"])

            if package_id in blocked_ids:
                return

            if package in final_packages:
                return

            final_packages.append(package)

            for dependency in package.get("dependencies", []):
                dependency_name, dependency_version = separate_name_from_version(dependency)

                for candidate in packages_found_list:
                    if candidate["name"] != dependency_name:
                        continue

                    if dependency_version:
                        if not compare_versions_symbols(dependency_version, candidate["version"]):
                            continue

                    add_package(candidate)
                    break

        for package in packages_to_check:
            add_package(package)

        packages_found_list = final_packages

    return packages_found_list, blocked_packages