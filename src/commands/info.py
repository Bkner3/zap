from src.db.database import get_package
from src.utils.versions_utils import separate_name_from_version


def info(packages):
    if not packages:
        print("No select packages!")
        return
    print("Package info:")
    for package in packages:
        name, version = separate_name_from_version(package)

        result = get_package(
            name,
            version if version is not False else None
        )

        if result is None:
            print(f"Package '{name}' not found!")
            continue

        name, version, author, description, dependencies, json_data = result[0]

        print(f"Name: {name} | Version: {version} | Author: {author} | Description: {description} | Dependencies: {dependencies}")