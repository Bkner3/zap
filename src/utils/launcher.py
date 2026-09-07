from platform import system
from src.utils.write_logs import log_info, log_warning
from src.utils.versions_utils import (
    separate_name_from_version,
    version_tuple,
    compare_versions_symbols
)
from src.zap_path import PathManager
import os


symlinks_path = PathManager.get("sl")
bin_path = PathManager.get("bin")


def find_available_version(index, dependency):
    dependency_name, required_version = separate_name_from_version(dependency)

    versions = []

    for package in index.get("packages", []):
        if package["name"] != dependency_name:
            continue

        version = str(package["version"])

        try:
            version_tuple(version)
            versions.append(version)
        except ValueError:
            pass

    if not versions:
        return False

    versions.sort(key=version_tuple, reverse=True)

    if required_version is False:
        return versions[0]

    for version in versions:
        if compare_versions_symbols(required_version, version):
            return version

    return False


def find_package(index, name, version):
    for package in index.get("packages", []):
        if (
            package["name"] == name
            and str(package["version"]) == str(version)
        ):
            return package

    return False


def resolve_dependencies(package, index, resolved=None, resolving=None):
    if resolved is None:
        resolved = []

    if resolving is None:
        resolving = []

    for dependency in package.get("dependencies", []) or []:
        dependency_name, dependency_requirement = separate_name_from_version(
            dependency
        )

        dependency_version = find_available_version(
            index,
            dependency
        )

        if dependency_version is False:
            log_warning(
                f"Could not resolve dependency: {dependency}"
            )
            continue

        dependency_key = (
            dependency_name,
            dependency_version
        )

        already_resolved = False

        for item in resolved:
            if (
                item["name"] == dependency_name
                and item["version"] == dependency_version
            ):
                already_resolved = True
                break

        if not already_resolved:
            resolved.append({
                "name": dependency_name,
                "version": dependency_version
            })

        if dependency_key in resolving:
            log_warning(
                f"Circular dependency detected: "
                f"{dependency_name}@{dependency_version}"
            )
            continue

        dependency_package = find_package(
            index,
            dependency_name,
            dependency_version
        )

        if dependency_package is False:
            log_warning(
                f"Package not found in index: "
                f"{dependency_name}@{dependency_version}"
            )
            continue

        resolving.append(dependency_key)

        resolve_dependencies(
            dependency_package,
            index,
            resolved,
            resolving
        )

        resolving.remove(dependency_key)

    return resolved


def find_latest_installed_version(name):
    package_bin_path = os.path.join(
        bin_path,
        name
    )

    if not os.path.isdir(package_bin_path):
        return False

    versions = []

    for folder in os.listdir(package_bin_path):
        folder_path = os.path.join(
            package_bin_path,
            folder
        )

        if os.path.isdir(folder_path):
            try:
                version_tuple(folder)
                versions.append(folder)
            except ValueError:
                pass

    if not versions:
        return False

    return max(versions, key=version_tuple)


def create_launcher(package, index):

    name = package["name"]
    version = str(package["version"])
    executable = package["exec_file"]

    install_folder = os.path.join(
        bin_path,
        name,
        version
    )

    executable_path = os.path.join(
        install_folder,
        executable
    )

    dependencies = resolve_dependencies(
        package,
        index
    )

    if system() == "Windows":

        package_sl_path = os.path.join(
            symlinks_path,
            name
        )

        version_sl_path = os.path.join(
            package_sl_path,
            version
        )

        os.makedirs(
            version_sl_path,
            exist_ok=True
        )

        path_entries = []

        for dependency in dependencies:
            dependency_path = os.path.join(
                symlinks_path,
                dependency["name"],
                dependency["version"]
            )

            path_entries.append(dependency_path)

        dependency_path_string = ";".join(path_entries)

        if dependency_path_string:
            dependency_path_string += ";"

        version_launcher = os.path.join(
            version_sl_path,
            f"{name}.bat"
        )

        version_script = f'''@echo off

set "root=%~dp0..\\..\\.."
set "bin_path=%root%\\bin"

if not defined PKG_ORIGINAL_PATH (
    set "PKG_ORIGINAL_PATH=%PATH%"
)

set "PATH={dependency_path_string}%PKG_ORIGINAL_PATH%"

"%root%\\bin\\{name}\\{version}\\{executable}" %*
'''

        with open(version_launcher, "w") as f:
            f.write(version_script)

        log_info(
            f"Writing launcher: {version_launcher}"
        )

        latest_version = find_latest_installed_version(name)

        if latest_version is False:
            latest_version = version

        latest_package = find_package(
            index,
            name,
            latest_version
        )

        if latest_package is not False:

            latest_dependencies = resolve_dependencies(
                latest_package,
                index
            )

            latest_path_entries = []

            for dependency in latest_dependencies:
                dependency_path = os.path.join(
                    symlinks_path,
                    dependency["name"],
                    dependency["version"]
                )

                latest_path_entries.append(
                    dependency_path
                )

            latest_dependency_path_string = ";".join(
                latest_path_entries
            )

            if latest_dependency_path_string:
                latest_dependency_path_string += ";"

            latest_launcher = os.path.join(
                symlinks_path,
                f"{name}.bat"
            )

            latest_script = f'''@echo off

set "root=%~dp0.."
set "bin_path=%root%\\bin"

if not defined PKG_ORIGINAL_PATH (
    set "PKG_ORIGINAL_PATH=%PATH%"
)

set "PATH={latest_dependency_path_string}%PKG_ORIGINAL_PATH%"

"%root%\\bin\\{name}\\{latest_version}\\{latest_package["exec_file"]}" %*
'''

            with open(latest_launcher, "w") as f:
                f.write(latest_script)

            log_info(
                f"Writing launcher: {latest_launcher}"
            )

    elif system() == "Linux":

        package_sl_path = os.path.join(
            symlinks_path,
            name
        )

        version_sl_path = os.path.join(
            package_sl_path,
            version
        )

        os.makedirs(
            version_sl_path,
            exist_ok=True
        )

        version_link = os.path.join(
            version_sl_path,
            name
        )

        if os.path.lexists(version_link):
            os.remove(version_link)

        os.symlink(
            executable_path,
            version_link
        )

        log_info(
            f"Creating symbolic link: {version_link}"
        )

        latest_version = find_latest_installed_version(name)

        if latest_version is False:
            latest_version = version

        latest_package = find_package(
            index,
            name,
            latest_version
        )

        if latest_package is not False:

            latest_executable = os.path.join(
                bin_path,
                name,
                latest_version,
                latest_package["exec_file"]
            )

            latest_link = os.path.join(
                symlinks_path,
                name
            )

            if os.path.lexists(latest_link):
                os.remove(latest_link)

            os.symlink(
                latest_executable,
                latest_link
            )

            log_info(
                f"Creating symbolic link: {latest_link}"
            )

        try:
            os.chmod(
                executable_path,
                0o755
            )
        except PermissionError:
            print(
                f"Warning: Could not change permissions "
                f"for {executable_path}"
            )

            log_warning(
                f"Warning: Could not change permissions "
                f"for {executable_path}"
            )


def remove_launcher(name, symlinks_path, system):

    launcher_path = (
        os.path.join(
            symlinks_path,
            f"{name}.bat"
        )
        if system == "Windows"
        else os.path.join(
            symlinks_path,
            name
        )
    )

    if system == "Windows":

        if os.path.exists(launcher_path):
            os.remove(launcher_path)

            log_info(
                f"Removing the symlink named: {name}"
            )
        else:
            print(
                f"Launcher not found: {name}.bat"
            )

            log_warning(
                f"Launcher not found: {name}.bat"
            )

    elif system == "Linux":

        if os.path.lexists(launcher_path):
            os.remove(launcher_path)

            log_info(
                f"Removing the symlink named: {name}"
            )
        else:
            print(
                f"Symlink not found: {name}"
            )

            log_warning(
                f"Symlink not found: {name}")