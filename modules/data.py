from database.connect import connect as connect_db

def load_data(table_name):
    conn = connect_db()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        queries = {
            'NhanVien': 'SELECT MaNV, HoLot, TenNV, Phai, NgaySinh, ChucVu FROM NhanVien',
            'KhachHang': 'SELECT MaKH, TenKH, SDT, DiaChi FROM KhachHang',
            'XeMay': 'SELECT MaXe, TenXe, LoaiXe, HangXe, GiaNhap, GiaBan, SoLuong FROM XeMay',
            'HoaDon': 'SELECT MaHD, NgayLap, MaNV, MaKH, MaXe, SoLuong, GiaBan, TongThanhTien FROM HoaDon'
        }
        sql = queries.get(table_name)
        if not sql:
            return []
        cur.execute(sql)
        rows = cur.fetchall()
        return [tuple(r) for r in rows]
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror('Lỗi', f'Lỗi tải dữ liệu {table_name}: {e}')
        return []
    finally:
        try:
            conn.close()
        except Exception:
            pass