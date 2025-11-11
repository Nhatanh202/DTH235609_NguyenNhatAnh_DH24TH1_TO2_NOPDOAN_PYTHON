("""CRUD helpers for table KhachHang.

Provides simple read functions using the shared `connect()` helper.
""")
import pyodbc
from database.connect import connect

TABLE_NAME = "KhachHang"


def load_all_data():
	"""Return all rows from KhachHang as a list of pyodbc.Row objects.

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
			print(f"Lỗi truy vấn load_all_data (KhachHang): {err}")
			return []
		finally:
			conn.close()
	return []


def get_by_id(makh):
	"""Return a single row for given MaKH or None if not found/error."""
	conn = connect()
	if conn:
		try:
			cursor = conn.cursor()
			sql = f"SELECT * FROM {TABLE_NAME} WHERE MaKH = ?"
			cursor.execute(sql, makh)
			row = cursor.fetchone()
			return row
		except pyodbc.Error as err:
			print(f"Lỗi truy vấn get_by_id (KhachHang): {err}")
			return None
		finally:
			conn.close()
	return None

