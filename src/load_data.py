
import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "marketing_attribution.db"

# Load parent tables before their dependent tables.
FILES = [
    ("channels.csv", "Channel"),
    ("campaigns.csv", "Campaign"),
    ("contacts.csv", "Contact"),
    ("touchpoints.csv", "Touchpoint"),
    ("web_sessions.csv", "WebSession"),
    ("leads.csv", "Lead"),
    ("opportunities.csv", "Opportunity"),
    ("orders.csv", "Order"),
    ("cost_records.csv", "CostRecord"),
    ("attribution_results.csv", "AttributionResult"),
]

# Clear dependent tables before parent tables when reloading.
DELETE_ORDER = [
    "AttributionResult",
    "Order",
    "Opportunity",
    "Lead",
    "WebSession",
    "Touchpoint",
    "CostRecord",
    "Contact",
    "Campaign",
    "Channel",
]


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Database not found. Run python src/setup_db.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # Clear previous generated records so reruns don't duplicate data.
        for table in DELETE_ORDER:
            conn.execute(f'DELETE FROM "{table}"')

        for filename, table in FILES:
            path = DATA_DIR / filename

            if not path.exists():
                raise FileNotFoundError(
                    f"Missing {filename}. Run generate_data.py first."
                )

            with path.open(
                "r", newline="", encoding="utf-8"
            ) as file:
                reader = csv.DictReader(file)
                columns = reader.fieldnames

                quoted_columns = ", ".join(
                    f'"{column}"' for column in columns
                )
                placeholders = ", ".join(
                    "?" for _ in columns
                )

                sql = (
                    f'INSERT INTO "{table}" ({quoted_columns}) '
                    f"VALUES ({placeholders})"
                )

                rows = [
                    tuple(
                        value if value != "" else None
                        for value in row.values()
                    )
                    for row in reader
                ]

                conn.executemany(sql, rows)
                print(f"Loaded {len(rows):,} rows into {table}")

    print("\nCSV data loaded into SQLite successfully!")


if __name__ == "__main__":
    main()
