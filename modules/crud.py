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
    if 'MaHD' not in data or not data['MaHD'].strip():
        data['MaHD'] = generate_mahd()
    
    maxe = data.get('MaXe', '').strip()
    so_luong_str = data.get('SoLuong', '').strip()
    gia_ban_str = data.get('GiaBan', '').strip()
    tong_tien_str = data.get('TongThanhTien', '').strip()
    if not all([maxe, so_luong_str.isdigit(), gia_ban_str.isdigit(), tong_tien_str.isdigit()]):
        messagebox.showwarning('Lỗi', 'Dữ liệu không hợp lệ')
        return False
    so_luong = int(so_luong_str)
    gia_ban = int(gia_ban_str)
    tong_tien = int(tong_tien_str)
    if tong_tien != gia_ban * so_luong:
        messagebox.showwarning('Lỗi', 'Tổng tiền không khớp')
        return False
    current_qty = get_quantity('XeMay', 'MaXe', maxe)
    if current_qty is None or current_qty < so_luong:
        messagebox.showwarning('Lỗi', 'Không đủ tồn kho')
        return False
    data.update({'SoLuong': so_luong, 'GiaBan': gia_ban, 'TongThanhTien': tong_tien})
    if not insert_record('HoaDon', data):
        messagebox.showerror('Lỗi', 'Không thể thêm hóa đơn vào cơ sở dữ liệu.')
        return False
    if not update_record('XeMay', {'SoLuong': current_qty - so_luong}, "MaXe = ?", (maxe,)):
        messagebox.showerror('Lỗi', 'Không thể cập nhật tồn kho.')
        return False
    messagebox.showinfo('Thành công', 'Đã thêm hóa đơn')
    return True