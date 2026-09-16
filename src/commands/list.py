from src.db.database import get_all_packages
from src.commands.config import read_config
from src.utils.write_logs import log_info, log_warning

def list_packages():
    packages = get_all_packages()
    if not packages:
        log_warning("No packages installed.")
        print("No packages installed.")
        return

    print("Package list:")
    log_info("Package list:")
    log_info(packages)

    config = read_config()
    show_json_data = config["show_json_data"]

    name_width = 12
    version_width = 10
    author_width = 15
    description_width = 50
    dependencies_width = 30
    json_data_with = 40

    print(
        f"{'Name':<{name_width}} | "
        f"{'Version':<{version_width}} | "
        f"{'Author':<{author_width}} | "
        f"{'Description':<{description_width}} | "
        f"{'Dependencies':<{dependencies_width}} |"
        f"{'Json-Data':<{json_data_with}}"
        if show_json_data else
        f"{'Name':<{name_width}} | "
        f"{'Version':<{version_width}} | "
        f"{'Author':<{author_width}} | "
        f"{'Description':<{description_width}} | "
        f"{'Dependencies':<{dependencies_width}}"
    )

    print(
        f"{'-' * name_width}-+-"
        f"{'-' * version_width}-+-"
        f"{'-' * author_width}-+-"
        f"{'-' * description_width}-+-"
        f"{'-' * dependencies_width}-+-"
        f"{'-' * json_data_with}"
        if show_json_data else
        f"{'-' * name_width}-+-"
        f"{'-' * version_width}-+-"
        f"{'-' * author_width}-+-"
        f"{'-' * description_width}-+-"
        f"{'-' * dependencies_width}"
    )

    for package in packages:
        name, version, author, description, dependencies, json_data = package

        print(
            f"{str(name):<{name_width}} | "
            f"{str(version):<{version_width}} | "
            f"{str(author):<{author_width}} | "
            f"{str(description):<{description_width}} | "
            f"{str(dependencies):<{dependencies_width}} |"
            f"{str(json_data):<{json_data_with}}"
            if show_json_data else
            f"{str(name):<{name_width}} | "
            f"{str(version):<{version_width}} | "
            f"{str(author):<{author_width}} | "
            f"{str(description):<{description_width}} | "
            f"{str(dependencies):<{dependencies_width}}"
        )
