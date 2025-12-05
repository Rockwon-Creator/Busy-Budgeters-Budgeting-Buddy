#!/usr/bin/env python3
"""
Load bank catalog rows from an Excel or CSV sheet into budgetbuddy.db.

"""

import os, csv, sqlite3, sys
from pathlib import Path

DB_PATH = Path("budgetbuddy.db")
SCHEMA_PATH = Path("schema.sql")

XLSX = Path("bank_catalog_htmlscope.xlsx")
CSV  = Path("bank_catalog_htmlscope.csv")

def to_float_or_none(x):
    if x is None: return None
    s = str(x).strip()
    if s == "" or s.lower() in {"n/a","na","none"}: return None
    s = s.replace("%","").replace("$","").replace(",","")
    try: return float(s)
    except: return None

def to_str_or_empty(x):
    """Return a clean string for any value, handling pandas NaN/Timestamp/etc."""
    try:
        import pandas as pd
        if pd.isna(x):
            return ""
    except Exception:
        pass
    if hasattr(x, "strftime"):
        return str(x)
    if x is None:
        return ""
    return str(x).strip()

def open_table_from_sheet():
    """
    Returns list of dict rows with the expected keys.
    Prefer .xlsx if present; else .csv.
    """
    cols = [
        "Bank","Product Type","Product Name","Compounding Frequency","Interest Basis",
        "APY (%)","Tiered APY Details (if any)","Min Deposit to Open ($)",
        "Monthly Maintenance Fee ($)","Fee Waiver Rule","ATM Out-of-Network Fee ($)",
        "Overdraft Fee ($)","Effective Date (YYYY-MM-DD)","Notes / Special Conditions","Source URL"
    ]
    if XLSX.exists():
        try:
            import pandas as pd  
        except ImportError:
            print("You have an .xlsx file but pandas/openpyxl not installed.\n"
                  "Install with:  pip3 install pandas openpyxl\n"
                  "Or save as CSV and use bank_catalog_htmlscope.csv instead.")
            sys.exit(1)
        df = pd.read_excel(XLSX)

        # --- Missing Colummns patch
        missing = [c for c in cols if c not in df.columns]
        if missing:
            print("⚠️  Warning: Missing optional columns:", missing)
            for col in missing:
                df[col] = None  

        return df.to_dict(orient="records")

    if CSV.exists():
        with open(CSV, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            missing = [c for c in cols if c not in r.fieldnames]
            if missing:
                print("⚠️  Warning: Missing optional columns:", missing)
            return list(r)

    print("Could not find sheet. Place one of these files next to this script:")
    print(" -", XLSX.name)
    print(" -", CSV.name)
    sys.exit(1)

def ensure_schema(conn: sqlite3.Connection):
    if SCHEMA_PATH.exists():
        conn.executescript(SCHEMA_PATH.read_text())

def get_or_create_bank(conn, name, website=None, phone=None):
    cur = conn.execute("SELECT bank_id FROM banks WHERE name=?", (name,))
    row = cur.fetchone()
    if row: return row[0]
    cur = conn.execute("INSERT INTO banks(name, website, support_phone) VALUES(?,?,?)",
                       (name, website, phone))
    conn.commit()
    return cur.lastrowid

def get_or_create_product(conn, bank_id, product_type, product_name, comp, basis, notes):
    cur = conn.execute("""
        SELECT product_id FROM bank_products
        WHERE bank_id=? AND product_type=? AND product_name=?""",
        (bank_id, product_type, product_name))
    row = cur.fetchone()
    if row:
        conn.execute("""UPDATE bank_products
                           SET compounding_freq=?, interest_basis=?, notes=?
                         WHERE product_id=?""",
                     (comp, basis, notes, row[0]))
        conn.commit()
        return row[0]
    cur = conn.execute("""INSERT INTO bank_products
          (bank_id, product_type, product_name, compounding_freq, interest_basis, notes)
           VALUES (?,?,?,?,?,?)""",
           (bank_id, product_type, product_name, comp, basis, notes))
    conn.commit()
    return cur.lastrowid

def upsert_terms(conn, product_id, eff_date, min_open, monthly_fee, waiver, atm_fee, overdraft, notes):
    # Close any current term row
    conn.execute("""
      UPDATE product_terms
         SET effective_end = date(?,'-1 day')
       WHERE product_id=? AND (effective_end IS NULL OR effective_end > ?)""",
       (eff_date, product_id, eff_date))
    # Insert new row
    conn.execute("""
      INSERT INTO product_terms
        (product_id, effective_start, effective_end, minimum_open_deposit,
         monthly_maintenance_fee, fee_waiver_rules, atm_out_of_network_fee,
         overdraft_fee, notes)
      VALUES (?,?,NULL,?,?,?,?,?,?)""",
      (product_id, eff_date, min_open, monthly_fee, waiver, atm_fee, overdraft, notes))
    conn.commit()

def upsert_single_rate(conn, product_id, eff_date, apy_percent):
    if apy_percent is None: return
    conn.execute("""
      UPDATE interest_rate_history
         SET effective_end = date(?,'-1 day')
       WHERE product_id=? AND (effective_end IS NULL OR effective_end > ?)""",
       (eff_date, product_id, eff_date))
    conn.execute("""
      INSERT INTO interest_rate_history(product_id, rate_percent, effective_start, effective_end)
      VALUES (?,?,?,NULL)""",
      (product_id, apy_percent, eff_date))
    conn.commit()

def load_rows(conn, rows):
    count = 0
    for r in rows:
        bank         = to_str_or_empty(r.get("Bank"))
        ptype        = to_str_or_empty(r.get("Product Type")).lower()
        pname        = to_str_or_empty(r.get("Product Name"))
        comp         = to_str_or_empty(r.get("Compounding Frequency")).lower()
        basis        = to_str_or_empty(r.get("Interest Basis")).lower()

        apy          = to_float_or_none(r.get("APY (%)"))
        min_open     = to_float_or_none(r.get("Min Deposit to Open ($)"))
        monthly_fee  = to_float_or_none(r.get("Monthly Maintenance Fee ($)"))
        waiver       = to_str_or_empty(r.get("Fee Waiver Rule"))
        atm_fee      = to_float_or_none(r.get("ATM Out-of-Network Fee ($)"))
        overdraft    = to_float_or_none(r.get("Overdraft Fee ($)"))

       
        eff_date_val = r.get("Effective Date (YYYY-MM-DD)")
        if hasattr(eff_date_val, "strftime"):
            eff_date = eff_date_val.strftime("%Y-%m-%d")
        else:
            eff_date = to_str_or_empty(eff_date_val) or "2025-11-01"

        
        notes        = to_str_or_empty(r.get("Notes / Special Conditions"))

        bank_id   = get_or_create_bank(conn, bank)
        product_id= get_or_create_product(conn, bank_id, ptype, pname, comp, basis, notes)

        upsert_terms(conn, product_id, eff_date, min_open, monthly_fee, waiver, atm_fee, overdraft, notes)
        upsert_single_rate(conn, product_id, eff_date, apy)

        count += 1
    return count

def main():
    conn = sqlite3.connect(DB_PATH.as_posix())
    try:
        conn.row_factory = sqlite3.Row
        ensure_schema(conn)
        rows = open_table_from_sheet()
        n = load_rows(conn, rows)
        print(f"Loaded/updated {n} products into {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
