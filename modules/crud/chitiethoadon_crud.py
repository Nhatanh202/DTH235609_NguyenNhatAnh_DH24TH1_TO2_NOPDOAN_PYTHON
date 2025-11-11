"""CRUD helpers for table ChiTietHoaDon.

Provides simple read functions using the shared `connect()` helper.
"""
import pyodbc
from database.connect import connect

TABLE_NAME = "ChiTietHD"


def load_all_data():
    """Return all rows from ChiTietHoaDon as a list of pyodbc.Row objects.

    Returns empty list on error.
    """
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {TABLE_NAME}")
            results = cursor.fetchall()
            return results
        except pyodbc.Error as err:
            print(f"Lỗi truy vấn load_all_data (ChiTietHoaDon): {err}")
            return []
        finally:
            conn.close()
    return []


def get_by_id(mahd, maxe):
    """Return a single row for given MaHD and MaXe or None if not found/error."""
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = f"SELECT * FROM {TABLE_NAME} WHERE MaHD = ? AND MaXe = ?"
            cursor.execute(sql, mahd, maxe)
            row = cursor.fetchone()
            return row
        except pyodbc.Error as err:
            print(f"Lỗi truy vấn get_by_id (ChiTietHoaDon): {err}")
            return None
        finally:
            conn.close()
    return None