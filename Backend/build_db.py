#!/usr/bin/env python3
import sqlite3, pathlib

DB_PATH = pathlib.Path("budgetbuddy.db")
SCHEMA_PATH = pathlib.Path("schema.sql")
SEED_PATH = pathlib.Path("seed_demo.sql")

def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH.as_posix())
    try:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.executescript(SEED_PATH.read_text())
        conn.commit()
        cur = conn.cursor()
        cur.execute("SELECT name FROM banks ORDER BY name;")
        print("Banks:", [r[0] for r in cur.fetchall()])
        cur.execute("""
          SELECT b.name, bp.product_type, bp.product_name
          FROM bank_products bp JOIN banks b ON b.bank_id=bp.bank_id
          ORDER BY b.name, bp.product_type, bp.product_name;
        """)
        rows = cur.fetchall()
        print(f"Products ({len(rows)}):")
        for r in rows:
            print(" -", r[0], "|", r[1], "|", r[2])
    finally:
        conn.close()
    print("Database created ->", DB_PATH.resolve())

if __name__ == "__main__":
    main()
