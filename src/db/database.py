import sqlite3
import os
from src.zap_path import PathManager


DB_PATH  = os.path.join(PathManager.get("data"), "zap.db")

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS packages (
        name TEXT PRIMARY KEY,
        version TEXT,
        description TEXT
    )
    """)

    conn.commit()
    conn.close()


def init_db():
    create_tables()


def reset_db():
    print("This will reset the database, all package information will be lost.")
    confirm = input("Are you sure? (y/n): ").strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS packages")
    conn.commit()
    conn.close()

    init_db()

    print("\nDatabase reset completed")


def recreate_db():
    pass


def save_package(name, version, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO packages (name, version, description)
    VALUES (?, ?, ?)
    ON CONFLICT(name) DO UPDATE SET
    version=excluded.version,
    description=excluded.description
    """, (name, version, description))

    conn.commit()
    conn.close()


def get_all_packages():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, version, description FROM packages")
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_package(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, version, description FROM packages WHERE name = ?", (name,))
    row = cursor.fetchone()

    conn.close()
    return row