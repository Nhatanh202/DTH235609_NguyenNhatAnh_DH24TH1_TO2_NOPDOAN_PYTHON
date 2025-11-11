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


def them_moi_khachhang(makh, tenkh, sdt, diachi):
    """Thêm mới khách hàng."""
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = f"INSERT INTO {TABLE_NAME} (MaKH, TenKH, SDT, DiaChi) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, makh, tenkh, sdt, diachi)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi thêm khách hàng: {err}")
            return False
        finally:
            conn.close()
    return False


def cap_nhat_khachhang(makh, tenkh, sdt, diachi):
    """Cập nhật thông tin khách hàng."""
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = f"UPDATE {TABLE_NAME} SET TenKH=?, SDT=?, DiaChi=? WHERE MaKH=?"
            cursor.execute(sql, tenkh, sdt, diachi, makh)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi cập nhật khách hàng: {err}")
            return False
        finally:
            conn.close()
    return False


def xoa_khachhang(makh):
    """Xóa khách hàng."""
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = f"DELETE FROM {TABLE_NAME} WHERE MaKH=?"
            cursor.execute(sql, makh)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi xóa khách hàng: {err}")
            return False
        finally:
            conn.close()
    return False