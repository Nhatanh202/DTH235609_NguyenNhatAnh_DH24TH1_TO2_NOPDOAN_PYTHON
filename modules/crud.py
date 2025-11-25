from database.connect import connect as connect_db
import tkinter.messagebox as messagebox

def execute_write(sql, params=None):
    conn = connect_db()
    if not conn:
        return False
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lỗi: {e}')
        return False
    finally:
        conn.close()

def insert_record(table_name, data):
    if not data:
        return False
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    return execute_write(sql, tuple(data.values()))

def update_record(table_name, data, where_clause, where_params):
    if not data:
        return False
    set_clause = ', '.join([f'{k}=?' for k in data.keys()])
    sql = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
    params = tuple(data.values()) + tuple(where_params)
    return execute_write(sql, params)

def delete_record(table_name, where_clause, where_params):
    sql = f'DELETE FROM {table_name} WHERE {where_clause}'
    return execute_write(sql, where_params)

def search_records(table_name, columns, search_term):
    if not search_term or not columns:
        return []
    conn = connect_db()
    if not conn:
        return []
    try:
        cur = conn.cursor()
        like_term = f"%{search_term}%"
        where_conditions = [f"CAST({col} AS NVARCHAR(MAX)) LIKE ?" for col in columns]
        where_clause = ' OR '.join(where_conditions)
        sql = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {where_clause}"
        params = tuple([like_term] * len(columns))
        cur.execute(sql, params)
        rows = cur.fetchall()
        return [tuple(row) for row in rows]
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lỗi tìm kiếm: {e}')
        return []
    finally:
        conn.close()

def get_quantity(table_name, id_column, id_value):
    conn = connect_db()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT SoLuong FROM {table_name} WHERE {id_column} = ?', (id_value,))
        result = cur.fetchone()
        return result[0] if result else None
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lỗi: {e}')
        return None
    finally:
        conn.close()

def generate_mahd():
    conn = connect_db()
    if not conn:
        return 'HD001'
    try:
        cur = conn.cursor()
        cur.execute("SELECT MAX(MaHD) FROM HoaDon WHERE MaHD LIKE 'HD%'")
        result = cur.fetchone()
        if result and result[0]:
            last_hd = result[0]
            num = int(last_hd[2:]) + 1
            return f'HD{num:03d}'
        else:
            return 'HD001'
    except Exception:
        return 'HD001'
    finally:
        conn.close()

def insert_hoa_don(data):
    """Thêm hóa đơn và cập nhật số lượng xe"""
    if 'MaHD' not in data or not data['MaHD'].strip():
        data['MaHD'] = generate_mahd()

    maxe = data.get('MaXe', '').strip()
    
    # Chuyển đổi các giá trị số, mặc định là 0 nếu rỗng hoặc không hợp lệ
    try:
        so_luong = int(data.get('SoLuong') or 0)
    except (ValueError, TypeError):
        so_luong = 0
        
    try:
        gia_ban = int(data.get('GiaBan') or 0)
    except (ValueError, TypeError):
        gia_ban = 0

    # Tính toán lại tổng tiền để đảm bảo chính xác
    tong_tien = so_luong * gia_ban
    data['TongThanhTien'] = tong_tien
    data['SoLuong'] = so_luong
    data['GiaBan'] = gia_ban

    if not maxe:
        messagebox.showwarning('Lỗi', 'Mã xe không được để trống.')
        return False
    if so_luong <= 0:
        messagebox.showwarning('Lỗi', 'Số lượng phải là số dương.')
        return False

    # Bắt đầu một transaction
    conn = connect_db()
    if not conn:
        messagebox.showerror('Lỗi', 'Không thể kết nối đến cơ sở dữ liệu.')
        return False
    
    try:
        cur = conn.cursor()
        # 1. Kiểm tra số lượng tồn kho
        cur.execute("SELECT SoLuong FROM XeMay WHERE MaXe = ?", (maxe,))
        result = cur.fetchone()
        current_qty = result[0] if result else 0

        if current_qty < so_luong:
            messagebox.showwarning('Lỗi', f'Không đủ hàng. Tồn kho chỉ còn {current_qty}.')
            conn.close()
            return False

        # 2. Thêm hóa đơn
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        sql_insert_hd = f'INSERT INTO HoaDon ({columns}) VALUES ({placeholders})'
        cur.execute(sql_insert_hd, tuple(data.values()))

        # 3. Cập nhật số lượng xe
        new_qty = current_qty - so_luong
        sql_update_xm = "UPDATE XeMay SET SoLuong = ? WHERE MaXe = ?"
        cur.execute(sql_update_xm, (new_qty, maxe))

        # Commit transaction
        conn.commit()
        messagebox.showinfo('Thành công', 'Đã thêm hóa đơn và cập nhật tồn kho thành công!')
        return True

    except Exception as e:
        conn.rollback() # Rollback nếu có lỗi
        messagebox.showerror('Lỗi Giao Dịch', f'Đã xảy ra lỗi: {e}. Giao dịch đã được hoàn tác.')
        return False
    finally:
        conn.close()