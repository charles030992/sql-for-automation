import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "empresa.db"
SQL_DIR = Path(__file__).parent.parent / "sql"


def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    schema = (SQL_DIR / "schema.sql").read_text(encoding="utf-8")
    cursor.executescript(schema)

    cursor.execute("SELECT COUNT(*) FROM vehiculos")
    if cursor.fetchone()[0] == 0:
        data = (SQL_DIR / "sample_data.sql").read_text(encoding="utf-8")
        cursor.executescript(data)

    conn.commit()
    conn.close()
    print(f"Database ready: {DB_PATH}")


if __name__ == "__main__":
    create_database()
