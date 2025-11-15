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
        messagebox.showerror('Lỗi', f'Lỗi thực thi: {e}')
        return False
    finally:
        try:
            conn.close()
        except Exception:
            pass

def insert_record(table_name, data):
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
    return execute_write(sql, tuple(data.values()))

def update_record(table_name, data, where_clause, where_params):
    set_clause = ', '.join([f'{k}=?' for k in data.keys()])
    sql = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause}'
    params = tuple(data.values()) + tuple(where_params)
    return execute_write(sql, params)

def delete_record(table_name, where_clause, where_params):
    sql = f'DELETE FROM {table_name} WHERE {where_clause}'
    return execute_write(sql, where_params)

def get_next_id(table_name, id_column):
    conn = connect_db()
    if not conn:
        return None
    try:
        cur = conn.cursor()
        cur.execute(f'SELECT MAX({id_column}) FROM {table_name}')
        max_id = cur.fetchone()[0]
        if max_id is None:
            return 1
        return max_id + 1
    except Exception as e:
        messagebox.showerror('Lỗi', f'Lỗi lấy ID tiếp theo: {e}')
        return None
    finally:
        try:
            conn.close()
        except Exception:
            pass