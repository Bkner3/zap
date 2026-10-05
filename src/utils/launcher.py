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
        if (package["name"] == name and str(package["version"]) == str(version)):
            return package

    return False


def resolve_dependencies(package, index, resolved=None, resolving=None):
    if resolved is None:
        resolved = []

    if resolving is None:
        resolving = []

    for dependency in package.get("dependencies", []) or []:
        dependency_name, dependency_requirement = separate_name_from_version(dependency)

        dependency_version = find_available_version(index, dependency)

        if dependency_version is False:
            log_warning(f"Could not resolve dependency: {dependency}")
            continue

        dependency_key = (dependency_name, dependency_version)

        already_resolved = False

        for item in resolved:
            if (item["name"] == dependency_name and item["version"] == dependency_version):
                already_resolved = True
                break

        if not already_resolved:
            resolved.append({
                "name": dependency_name,
                "version": dependency_version
            })

        if dependency_key in resolving:
            log_warning(f"Circular dependency detected: {dependency_name}@{dependency_version}")
            continue

        dependency_package = find_package(index, dependency_name, dependency_version)

        if dependency_package is False:
            log_warning(f"Package not found in index: {dependency_name}@{dependency_version}")
            continue

        resolving.append(dependency_key)

        resolve_dependencies(dependency_package, index, resolved, resolving)

        resolving.remove(dependency_key)

    return resolved


def find_latest_installed_version(name):
    package_bin_path = os.path.join(bin_path, name)

    if not os.path.isdir(package_bin_path):
        return False

    versions = []

    for folder in os.listdir(package_bin_path):
        folder_path = os.path.join(package_bin_path, folder)

        if os.path.isdir(folder_path):
            try:
                version_tuple(folder)
                versions.append(folder)
            except ValueError:
                pass

    if not versions:
        return False

    return max(versions, key=version_tuple)


def find_direct_dependencies(package, index):
    dependencies = []

    for dependency in package.get("dependencies", []) or []:
        dependency_name, dependency_requirement = separate_name_from_version(dependency)

        dependency_version = find_available_version(index, dependency)

        if dependency_version is False:
            log_warning(f"Could not resolve dependency: {dependency}")
            continue

        dependencies.append({"name": dependency_name, "version": dependency_version})

    return dependencies


def create_launcher(package, index):
    name = package["name"]
    version = str(package["version"])
    executable = package["exec_file"]
    executable_on_bin_path = os.path.join(bin_path, name, version, executable)

    dependencies = find_direct_dependencies(package, index)

    if system() == "Windows":
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

        package_sl_path = os.path.join(symlinks_path, name)
        version_sl_path = os.path.join(package_sl_path, version)

        os.makedirs(version_sl_path, exist_ok=True)

        version_launcher = os.path.join(
            version_sl_path,
            f"{name}.cmd"
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

        log_info(f"Writing launcher: {version_launcher}")

        latest_version = find_latest_installed_version(name)

        if latest_version is False:
            latest_version = version

        latest_package = find_package(index, name, latest_version)

        if latest_package is not False:
            latest_dependencies = find_direct_dependencies(
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
                latest_path_entries.append(dependency_path)

            latest_dependency_path_string = ";".join(latest_path_entries)
            if latest_dependency_path_string:
                latest_dependency_path_string += ";"

            latest_launcher = os.path.join(
                symlinks_path,
                f"{name}.cmd"
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

            log_info(f"Writing launcher: {latest_launcher}")

    elif system() == "Linux":
        path_entries = []
        for dependency in dependencies:
            dependency_path = os.path.join(
                symlinks_path,
                dependency["name"],
                dependency["version"]
            )
            path_entries.append(dependency_path)

        dependency_path_string = ":".join(path_entries)
        if dependency_path_string:
            dependency_path_string += ":"

        package_sl_path = os.path.join(symlinks_path, f"_{name}")
        version_sl_path = os.path.join(package_sl_path, version)
        os.makedirs(version_sl_path, exist_ok=True)

        version_launcher = os.path.join(version_sl_path, name)

        version_script = f'''#!/bin/bash

script_dir="$(cd -- "$(dirname -- "${{BASH_SOURCE[0]}}")" && pwd)"
root="$(cd -- "$script_dir/../../.." && pwd)"

if [ -z "${{PKG_ORIGINAL_PATH+x}}" ]; then
    export PKG_ORIGINAL_PATH="$PATH"
fi

export PATH="{dependency_path_string}$PKG_ORIGINAL_PATH"

exec "$root/bin/{name}/{version}/{executable}" "$@"
'''

        with open(version_launcher, "w") as f:
            f.write(version_script)

        os.chmod(version_launcher, 0o755)
        log_info(f"Writing launcher: {version_launcher}")

        latest_version = find_latest_installed_version(name)
        if latest_version is False:
            latest_version = version

        latest_launcher_target = os.path.join(symlinks_path, f"{name}")

        if os.path.islink(latest_launcher_target) or os.path.exists(latest_launcher_target):
            os.remove(latest_launcher_target)
        if os.path.exists(executable_on_bin_path):
            current_mode = os.stat(executable_on_bin_path).st_mode
            os.chmod(executable_on_bin_path, current_mode | os.stat.S_IXUSR | os.stat.S_IXGRP | os.stat.S_IXOTH)
        os.symlink(version_launcher, latest_launcher_target)


def remove_launcher(name_arg):
    name, version = separate_name_from_version(name_arg)

    launcher_path = (
        os.path.join(symlinks_path, f"{name}.cmd")
        if system() == "Windows"
        else os.path.join(symlinks_path, name)
    )

    if version is not None and version is not False:
        v_launcher = (
            os.path.join(
                str(symlinks_path),
                str(name),
                str(version),
                f"{name}.cmd"
            )
            if system() == "Windows"
            else os.path.join(
                str(symlinks_path),
                f"_{str(name)}",
                str(version),
                str(name)
            )
        )

    if system() == "Windows":
        if os.path.exists(launcher_path):
            os.remove(launcher_path)

        if version is not None and version is not False:
            if os.path.exists(v_launcher):
                os.remove(v_launcher)
                log_info(f"Removing the launcher named: {name}")
            else:
                print(f"Launcher not found: {name}.cmd")
                log_warning(f"Launcher not found: {name}.cmd")

    elif system() == "Linux":
        if version is not None and version is not False:
            if os.path.lexists(v_launcher):
                os.remove(v_launcher)
                log_info(f"Removing launcher version: {name}@{version}")

                # Atualizar ou remover o symlink principal se foi removida a versão ativa
                latest_version = find_latest_installed_version(name)
                if latest_version:
                    new_target = os.path.join(symlinks_path, name, latest_version, name)
                    if os.path.lexists(launcher_path):
                        os.remove(launcher_path)
                    os.symlink(os.path.relpath(new_target, symlinks_path), launcher_path)
                elif os.path.lexists(launcher_path):
                    os.remove(launcher_path)
            else:
                print(f"Launcher not found: {name}@{version}")
                log_warning(f"Launcher not found: {name}@{version}")
        else:
            if os.path.lexists(launcher_path):
                os.remove(launcher_path)
                log_info(f"Removing main symlink/launcher: {name}")
            else:
                print(f"Symlink not found: {name}")
                log_warning(f"Symlink not found: {name}")