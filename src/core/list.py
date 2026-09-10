from src.db.database import get_all_packages
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

    # Largura de cada coluna
    name_width = 12
    version_width = 10
    author_width = 15
    description_width = 25
    dependencies_width = 25

    # Cabeçalho
    print(
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
        f"{'-' * dependencies_width}"
    )

    # Pacotes
    for package in packages:
        name, version, author, description, dependencies = package

        print(
            f"{str(name):<{name_width}} | "
            f"{str(version):<{version_width}} | "
            f"{str(author):<{author_width}} | "
            f"{str(description):<{description_width}} | "
            f"{str(dependencies):<{dependencies_width}}"
        )
