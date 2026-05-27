import sqlite3
import os
from src.zap_path import PathManager

DB_PATH = os.path.join(PathManager.get("data"), "zap.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS packages (
            name TEXT PRIMARY KEY,
            version TEXT,
            description TEXT
        )
        """)

        conn.commit()


def init_db():
    create_tables()


def reset_db():
    print("This will reset the database, all package information will be lost.")
    confirm = input("Are you sure? (y/n): ").strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS packages")

        conn.commit()

    init_db()

    print("\nDatabase reset completed")


def recreate_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS packages")

        conn.commit()

    init_db()

    print("Database recreated.")


def save_package(name, version, description):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO packages (name, version, description)
        VALUES (?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            version = excluded.version,
            description = excluded.description
        """, (name, version, description))

        conn.commit()


def get_all_packages():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT name, version, description
        FROM packages
        """)

        return cursor.fetchall()


def get_package(name):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT name, version, description
        FROM packages
        WHERE name = ?
        """, (name,))

        return cursor.fetchone()


def delete_package(name):
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM packages
        WHERE name = ?
        """, (name,))

        conn.commit()

        if cursor.rowcount > 0:
            print(f"Package {name} removed from the database.")
        else:
            print(f"Package {name} not found on the database.")
