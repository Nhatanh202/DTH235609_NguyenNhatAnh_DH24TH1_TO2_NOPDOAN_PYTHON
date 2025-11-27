from tkinter import *
from tkinter import ttk, messagebox
import hashlib
import utils

def create_ui(parent_frame):
    try:
        # --- 1. BIẾN DỮ LIỆU ---
        parent_frame.vars = {}
        
        var_username = StringVar()
        var_vaitro = StringVar()
        
        var_pass_old = StringVar()
        var_pass_new = StringVar()
        var_pass_confirm = StringVar()

        BG_COLOR = getattr(utils, 'MAIN_BG', 'white')
        
        # Lấy thông tin an toàn (tránh lỗi nếu utils chưa có biến)
        current_id = utils.current_user.get('id', '')     
        current_role = utils.current_user.get('role', '') 

        # --- 2. HÀM XỬ LÝ ---
        def load_info():
            var_vaitro.set(current_role if current_role else "---")
            if current_id:
                try:
                    conn = utils.get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT TenDangNhap FROM TaiKhoan WHERE MaNhanVien=?", (current_id,))
                    row = cursor.fetchone()
                    if row: var_username.set(row[0])
                    else: var_username.set("---")
                    conn.close()
                except: var_username.set("Error DB")
            else:
                var_username.set("Chưa đăng nhập")

        def act_doi_mat_khau():
            old = var_pass_old.get()
            new = var_pass_new.get()
            confirm = var_pass_confirm.get()
            user = var_username.get()

            if not old or not new or not confirm:
                return messagebox.showwarning("Thiếu tin", "Nhập đủ mật khẩu!")
            if new != confirm:
                return messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp!")
            
            try:
                conn = utils.get_connection()
                cursor = conn.cursor()
                hashed_old = hashlib.sha256(old.encode()).hexdigest()
                cursor.execute("SELECT MatKhau FROM TaiKhoan WHERE TenDangNhap=?", (user,))
                row = cursor.fetchone()
                
                if not row or row[0] != hashed_old:
                    return messagebox.showerror("Lỗi", "Mật khẩu cũ sai!")

                hashed_new = hashlib.sha256(new.encode()).hexdigest()
                cursor.execute("UPDATE TaiKhoan SET MatKhau=? WHERE TenDangNhap=?", (hashed_new, user))
                conn.commit()
                conn.close()
                messagebox.showinfo("OK", "Đổi mật khẩu thành công!")
                var_pass_old.set(""); var_pass_new.set(""); var_pass_confirm.set("")
            except Exception as e:
                messagebox.showerror("Lỗi SQL", str(e))

        # --- 3. GIAO DIỆN ---
        Label(parent_frame, text="THÔNG TIN TÀI KHOẢN", font=("Arial", 20, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=20)

        # Khung Thông tin
        fr_info = LabelFrame(parent_frame, text="Thông tin tài khoản", font=("Arial", 11, "bold"), bg=BG_COLOR, padx=20, pady=15)
        fr_info.pack(fill=X, padx=50, pady=10)

        Label(fr_info, text="Tên đăng nhập:", font=("Arial", 11), bg=BG_COLOR).grid(row=0, column=0, sticky=W, pady=8)
        Label(fr_info, textvariable=var_username, font=("Arial", 12, "bold"), fg="blue", bg=BG_COLOR).grid(row=0, column=1, sticky=W, padx=20)

        Label(fr_info, text="Chức vụ:", font=("Arial", 11), bg=BG_COLOR).grid(row=1, column=0, sticky=W, pady=8)
        Label(fr_info, textvariable=var_vaitro, font=("Arial", 12, "bold"), fg="red", bg=BG_COLOR).grid(row=1, column=1, sticky=W, padx=20)

        # Khung Đổi mật khẩu
        fr_pass = LabelFrame(parent_frame, text="Đổi Mật Khẩu", font=("Arial", 11, "bold"), bg=BG_COLOR, padx=20, pady=15)
        fr_pass.pack(fill=X, padx=50, pady=10)

        def make_entry(lbl, var, r):
            Label(fr_pass, text=lbl, font=("Arial", 11), bg=BG_COLOR).grid(row=r, column=0, sticky=W, pady=8)
            Entry(fr_pass, textvariable=var, show="*", width=35).grid(row=r, column=1, sticky=W, padx=20)

        make_entry("Mật khẩu cũ:", var_pass_old, 0)
        make_entry("Mật khẩu mới:", var_pass_new, 1)
        make_entry("Nhập lại mới:", var_pass_confirm, 2)

        Button(fr_pass, text="LƯU MẬT KHẨU", command=act_doi_mat_khau, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=20, height=2).grid(row=3, column=1, pady=20, sticky=W, padx=20)

        load_info()

    except Exception as e:
        # Nếu có lỗi, hiện lên màn hình để biết đường sửa
        Label(parent_frame, text=f"Lỗi hiển thị: {e}", fg="red", font=("Arial", 14)).pack(pady=50)