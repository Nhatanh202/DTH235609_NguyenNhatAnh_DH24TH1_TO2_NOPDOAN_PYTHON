from __future__ import annotations
import os
from typing import Optional

try:
    import pyodbc
except Exception:  # ImportError or others
    pyodbc = None


DEFAULT_CONN = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=LAPTOP-08CQM6N0;"
    "DATABASE=QUANLYCUAHANGXEMAY;"
    "Trusted_Connection=yes;"
)


def connect(connection_string: Optional[str] = None, autocommit: bool = False):
    if connection_string is None:
        connection_string = os.getenv("DB_CONN_STRING", DEFAULT_CONN)

    if pyodbc is None:
        raise RuntimeError(
            "pyodbc is not installed. Install it with: pip install pyodbc"
        )

    try:
        conn = pyodbc.connect(connection_string)
        conn.autocommit = autocommit
        return conn
    except Exception as exc:
        print("[connect] failed to open DB connection:", exc)
        return None


if __name__ == "__main__":
    conn = connect()
    if not conn:
        print("Connection failed")
    else:
        try:
            cur = conn.cursor()
            cur.execute("SELECT TOP 5 name FROM sys.tables")
            for row in cur:
                print(row)
        finally:
            conn.close()