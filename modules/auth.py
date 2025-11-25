import os
import hashlib
from database.connect import connect as connect_db

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_login(username, password):
    conn = connect_db()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Admin special-case: try DB table then file then default
        if username.lower() == 'admin':
            try:
                cursor.execute("SELECT MatKhau FROM TaiKhoan WHERE TenDangNhap = ?", ('admin',))
                r = cursor.fetchone()
                if r:
                    return str(r[0]) == hash_password(password)
            except Exception:
                pass

            admin_file = os.path.join(os.path.dirname(__file__), '.admin_pass')
            if os.path.exists(admin_file):
                try:
                    with open(admin_file, 'r', encoding='utf-8') as f:
                        stored = f.read().strip()
                        return stored == hash_password(password)
                except Exception:
                    return False
            return hash_password(password) == hash_password('123')

        # Normal employee: password is TenNV in DB; allow username as MaNV or TenNV
        cursor.execute("SELECT MaNV, TenNV FROM NhanVien WHERE MaNV = ? OR TenNV = ?", (username, username))
        row = cursor.fetchone()
        if not row:
            return False
        db_manv, db_tennv = row[0], row[1]
        # Accept if password equals TenNV and username matches either MaNV or TenNV
        if hash_password(db_tennv) == hash_password(password) and (str(db_manv) == str(username) or str(db_tennv) == str(username)):
            return True
        return False
    except Exception as e:
        # Log error instead of showing GUI message in auth module
        print(f"Lỗi kiểm tra đăng nhập: {e}")
        return False
    finally:
        try:
            conn.close()
        except Exception:
            pass

def update_admin_password(current_pass, new_pass):
    """Cập nhật mật khẩu admin: if TaiKhoan table exists update it else write .admin_pass"""
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            try:
                cur.execute("SELECT MatKhau FROM TaiKhoan WHERE TenDangNhap = ?", ('admin',))
                _ = cur.fetchone()
                # Try update else insert
                try:
                    cur.execute("UPDATE TaiKhoan SET MatKhau = ? WHERE TenDangNhap = ?", (hash_password(new_pass), 'admin'))
                    if cur.rowcount == 0:
                        cur.execute("INSERT INTO TaiKhoan (TenDangNhap, MatKhau) VALUES (?, ?)", ('admin', hash_password(new_pass)))
                except Exception:
                    # fallback to file
                    conn.commit()
                    conn.close()
                    raise
                conn.commit()
                conn.close()
                return True, 'Cập nhật mật khẩu thành công (DB)'
            except Exception:
                try:
                    conn.close()
                except Exception:
                    pass
        except Exception:
            try:
                conn.close()
            except Exception:
                pass

    # fallback to file
    admin_file = os.path.join(os.path.dirname(__file__), '.admin_pass')
    try:
        with open(admin_file, 'w', encoding='utf-8') as f:
            f.write(hash_password(new_pass))
        return True, 'Cập nhật mật khẩu thành công (file)'
    except Exception as e:
        return False, f'Lỗi khi lưu mật khẩu: {e}'