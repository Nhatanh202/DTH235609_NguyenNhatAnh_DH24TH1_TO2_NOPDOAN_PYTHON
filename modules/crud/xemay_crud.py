import pyodbc
from database.connect import connect # Import hàm kết nối SQL Server

# Tên bảng trong SQL Server
TABLE_NAME = "XeMay" 

# --- HÀM 1: READ (Tải dữ liệu) ---
def load_all_data():
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            # Lệnh SELECT lấy tất cả dữ liệu
            cursor.execute(f"SELECT MaXe, TenXe, LoaiXe, HangXe, GiaNhap, NgayNhap, SoKhung, TinhTrang FROM {TABLE_NAME}")
            results = cursor.fetchall()
            return results
        except pyodbc.Error as err:
            print(f"Lỗi truy vấn Load Data: {err}")
            return []
        finally:
            conn.close()
    return []

# --- HÀM 2: CREATE (Thêm mới) ---
def them_moi_xe(maxe, tenxe, loaixe, hangxe, gianhap, ngaynhap, sokhung, tinhtrang):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            # Lệnh INSERT INTO SQL Server
            sql = f"INSERT INTO {TABLE_NAME} (MaXe, TenXe, LoaiXe, HangXe, GiaNhap, NgayNhap, SoKhung, TinhTrang) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            
            # Chú ý: Dùng dấu '?' (placeholder) cho pyodbc, giá trị được truyền qua tuple
            cursor.execute(sql, maxe, tenxe, loaixe, hangxe, gianhap, ngaynhap, sokhung, tinhtrang)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi thêm xe: {err}")
            return False
        finally:
            conn.close()
    return False

# --- HÀM 3: UPDATE (Sửa đổi) ---
def cap_nhat_xe(maxe, tenxe, loaixe, hangxe, gianhap, ngaynhap, sokhung, tinhtrang):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            # Lệnh UPDATE SQL Server
            sql = f"""
            UPDATE {TABLE_NAME} SET 
                TenXe=?, LoaiXe=?, HangXe=?, GiaNhap=?, NgayNhap=?, SoKhung=?, TinhTrang=?
            WHERE MaXe=?
            """
            cursor.execute(sql, tenxe, loaixe, hangxe, gianhap, ngaynhap, sokhung, tinhtrang, maxe)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi cập nhật xe: {err}")
            return False
        finally:
            conn.close()
    return False

# --- HÀM 4: DELETE (Xóa) ---
def xoa_xe(maxe):
    conn = connect()
    if conn:
        try:
            cursor = conn.cursor()
            sql = f"DELETE FROM {TABLE_NAME} WHERE MaXe=?"
            cursor.execute(sql, maxe)
            conn.commit()
            return True
        except pyodbc.Error as err:
            print(f"Lỗi xóa xe: {err}")
            return False
        finally:
            conn.close()
    return False