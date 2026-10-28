
import sqlite3
from pathlib import Path

# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# File locations
SCHEMA_PATH = BASE_DIR / "src" / "schema.sql"
DB_PATH = BASE_DIR / "data" / "marketing_attribution.db"


def main():
    # Create the data folder if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read the SQL schema
    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    # Create the database and tables
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(schema)

        tables = conn.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """).fetchall()

    print("Database created successfully!")
    print(f"Database location: {DB_PATH}")
    print(f"Number of tables: {len(tables)}")

    for (table_name,) in tables:
        print("-", table_name)


if __name__ == "__main__":
    main()
