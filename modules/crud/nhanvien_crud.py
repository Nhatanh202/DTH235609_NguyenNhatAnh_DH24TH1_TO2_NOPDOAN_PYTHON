
"""CRUD helpers for table NhanVien.

Provides simple read functions using the shared `connect()` helper.
"""
import pyodbc
from database.connect import connect

TABLE_NAME = "NhanVien"


def load_all_data():
	"""Return all rows from NhanVien as a list of pyodbc.Row objects.

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
			print(f"Lỗi truy vấn load_all_data (NhanVien): {err}")
			return []
		finally:
			conn.close()
	return []


def get_by_id(manv):
	"""Return a single row for given MaNV or None if not found/error."""
	conn = connect()
	if conn:
		try:
			cursor = conn.cursor()
			sql = f"SELECT * FROM {TABLE_NAME} WHERE MaNV = ?"
			cursor.execute(sql, manv)
			row = cursor.fetchone()
			return row
		except pyodbc.Error as err:
			print(f"Lỗi truy vấn get_by_id (NhanVien): {err}")
			return None
		finally:
			conn.close()
	return None

