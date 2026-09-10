import sqlite3
import os

from src.zap_path import PathManager
from src.utils.write_logs import log_info, log_warning, log_debug


DB_PATH = os.path.join(PathManager.get("data"), "zap.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    log_info("Creating the DataBase tables.")

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            author TEXT,
            description TEXT,
            dependencies TEXT,
            PRIMARY KEY (name, version)
        )
        """)

        conn.commit()


def init_db():
    log_info("Inicializing the DataBase")
    create_tables()


def reset_db():
    log_warning(
        "reset_db was called. If confirmed by the user, "
        "the database will be reset."
    )

    print("This will reset the database, all package information will be lost.")
    confirm = input("Are you sure? (y/n): ").strip().lower()

    if confirm != "y":
        log_info("Cancelled")
        print("Cancelled.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS packages")

        conn.commit()

    init_db()

    log_warning("Database reset completed")
    print("\nDatabase reset completed")


def recreate_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS packages")

        conn.commit()

    init_db()
    log_info("Database recreated.")
    print("Database recreated.")

def save_package(name, version, author, description, dependencies=None):
    init_db()
    log_info(
        f"Saving {name} {version} by {author} to the DataBase"
    )

    if isinstance(dependencies, list):
        dependencies = ", ".join(dependencies)

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO packages (
            name,
            version,
            author,
            description,
            dependencies
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(name, version) DO UPDATE SET
            author = excluded.author,
            description = excluded.description,
            dependencies = excluded.dependencies
        """, (
            name,
            version,
            author,
            description,
            dependencies
        ))

        conn.commit()


def get_all_packages():
    init_db()
    log_info("Returning all packages registered in the database")
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            name,
            version,
            author,
            description,
            dependencies
        FROM packages
        ORDER BY name, version
        """)

        return cursor.fetchall()


def get_package(name, version=None):
    init_db()

    with get_connection() as conn:
        cursor = conn.cursor()

        if version is not None:
            cursor.execute("""
            SELECT
                name,
                version,
                author,
                description,
                dependencies
            FROM packages
            WHERE name = ? AND version = ?
            """, (name, version))

            result = cursor.fetchone()

        else:
            cursor.execute("""
            SELECT
                name,
                version,
                author,
                description,
                dependencies
            FROM packages
            WHERE name = ?
            ORDER BY version
            """, (name,))

            result = cursor.fetchall()

        if result:
            log_info(
                f"Returning information for package '{name}'"
            )
        else:
            log_warning(
                f"Package '{name}' not found"
            )

        return result


def delete_package(name, version=None):
    init_db()

    with get_connection() as conn:
        cursor = conn.cursor()

        if version is not None:
            cursor.execute("""
            DELETE FROM packages
            WHERE name = ? AND version = ?
            """, (name, version))

            deleted_message = f"Package {name} {version} removed from the database."
            not_found_message = f"Package {name} {version} not found on the database."

        else:
            cursor.execute("""
            DELETE FROM packages
            WHERE name = ?
            """, (name,))

            deleted_message = f"All versions of package {name} removed from the database."
            not_found_message = f"Package {name} not found on the database."

        conn.commit()

        if cursor.rowcount > 0:
            log_info(deleted_message)
            print(deleted_message)
        else:
            log_warning(not_found_message)
            print(not_found_message)

