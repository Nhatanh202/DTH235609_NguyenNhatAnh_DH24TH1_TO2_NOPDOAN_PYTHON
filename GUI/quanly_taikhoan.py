from tkinter import *
from tkinter import ttk, messagebox
import hashlib # Thư viện mã hóa mật khẩu
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    parent_frame.vars = {}
    
    var_user = StringVar()
    var_pass = StringVar()
    var_vaitro = StringVar()
    var_search = StringVar()
    
    # Biến Combobox chọn Nhân viên
    var_cbb_nv = StringVar()
    
    # Map: "Tên NV (Mã)" -> "Mã NV"
    map_nv = {}

    current_mode = "VIEW"
    BG_COLOR = getattr(utils, 'MAIN_BG', 'white')

    # --- 2. HÀM DATABASE ---
    def load_combobox_nv():
        """Load danh sách nhân viên để tạo tài khoản"""
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()
            
            # Lấy tất cả nhân viên đang làm việc
            cursor.execute("SELECT MaNhanVien, HoVaTen FROM NhanVien WHERE TrangThai=1")
            
            map_nv.clear()
            cbb_nv['values'] = []
            list_nv = []
            
            for row in cursor.fetchall():
                display = f"{row[1]} ({row[0]})" # Tên (Mã)
                map_nv[display] = row[0]
                list_nv.append(display)
            
            cbb_nv['values'] = list_nv
            conn.close()
        except Exception as e:
            print(f"Lỗi load NV: {e}")

    def load_data(search_txt=None):
        for item in tree.get_children(): tree.delete(item)
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()
            
            # Kết nối bảng TaiKhoan và NhanVien để lấy tên hiển thị
            sql = """
                SELECT tk.TenDangNhap, nv.HoVaTen, tk.VaiTro, nv.MaNhanVien
                FROM TaiKhoan tk
                JOIN NhanVien nv ON tk.MaNhanVien = nv.MaNhanVien
            """
            params = []
            
            if search_txt and search_txt.strip() != "":
                sql += " WHERE tk.TenDangNhap LIKE ? OR nv.HoVaTen LIKE ?"
                kw = f"%{search_txt}%"
                params = [kw, kw]
                
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            for row in rows:
                # Ẩn mật khẩu, không load lên bảng
                tree.insert("", END, values=(row[0], row[1], row[2], row[3]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def act_luu():
        user = var_user.get().strip()
        pwd_raw = var_pass.get().strip()
        txt_nv = var_cbb_nv.get()
        role = var_vaitro.get()

        # Validate cơ bản
        if not user:
            return messagebox.showwarning("Cảnh báo", "Tên đăng nhập là bắt buộc!")
        if not txt_nv:
            return messagebox.showwarning("Cảnh báo", "Vui lòng chọn Nhân viên sở hữu tài khoản!")
        if not role:
            return messagebox.showwarning("Cảnh báo", "Vui lòng chọn Vai trò!")

        # Lấy Mã NV từ Map
        try:
            ma_nv = map_nv.get(txt_nv)
            if not ma_nv: raise ValueError
        except:
            return messagebox.showwarning("Lỗi chọn", "Nhân viên không hợp lệ. Hãy chọn từ danh sách!")

        conn = utils.get_connection()
        cursor = conn.cursor()
        
        try:
            if current_mode == "ADD":
                if not pwd_raw:
                    return messagebox.showwarning("Cảnh báo", "Mật khẩu không được để trống khi tạo mới!")
                
                # Check trùng user
                cursor.execute("SELECT Count(*) FROM TaiKhoan WHERE TenDangNhap=?", (user,))
                if cursor.fetchone()[0] > 0:
                    return messagebox.showerror("Trùng lặp", f"Tài khoản '{user}' đã tồn tại!")

                # 1. Mã hóa mật khẩu
                hashed_pw = hashlib.sha256(pwd_raw.encode()).hexdigest()
                
                # 2. Insert
                sql = "INSERT INTO TaiKhoan (TenDangNhap, MatKhau, MaNhanVien, VaiTro) VALUES (?, ?, ?, ?)"
                cursor.execute(sql, (user, hashed_pw, ma_nv, role))
                messagebox.showinfo("Thành công", "Đã tạo tài khoản mới!")

            elif current_mode == "EDIT":
                # Logic Sửa:
                # - Nếu ô Mật khẩu để TRỐNG -> Giữ nguyên mật khẩu cũ (Không update cột MatKhau)
                # - Nếu ô Mật khẩu có chữ -> Mã hóa và Cập nhật mật khẩu mới
                
                if pwd_raw: # Có nhập pass mới
                    hashed_pw = hashlib.sha256(pwd_raw.encode()).hexdigest()
                    sql = "UPDATE TaiKhoan SET MatKhau=?, MaNhanVien=?, VaiTro=? WHERE TenDangNhap=?"
                    cursor.execute(sql, (hashed_pw, ma_nv, role, user))
                    msg = "Đã cập nhật thông tin và mật khẩu!"
                else: # Không nhập pass -> Giữ cũ
                    sql = "UPDATE TaiKhoan SET MaNhanVien=?, VaiTro=? WHERE TenDangNhap=?"
                    cursor.execute(sql, (ma_nv, role, user))
                    msg = "Đã cập nhật thông tin (Giữ nguyên mật khẩu)!"
                
                messagebox.showinfo("Thành công", msg)

            conn.commit()
            click_huy()
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def click_xoa():
        user = var_user.get()
        if not user: return
        
        if user.lower() == 'admin':
            return messagebox.showwarning("Cấm", "Không thể xóa tài khoản Admin gốc!")

        if messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa tài khoản '{user}'?"):
            try:
                conn = utils.get_connection()
                conn.execute("DELETE FROM TaiKhoan WHERE TenDangNhap=?", (user,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa tài khoản.")
                click_huy()
                load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # --- 3. UI CONTROL ---
    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        st_entry = "normal" if mode != "VIEW" else "readonly"
        st_cbb = "readonly" if mode != "VIEW" else "disabled"
        
        # Tên đăng nhập: Khóa khi Sửa (là Khóa chính)
        entry_user.config(state="normal" if mode == "ADD" else "readonly")
        
        entry_pass.config(state="normal" if mode in ["ADD", "EDIT"] else "readonly")
        cbb_nv.config(state=st_cbb)
        cbb_role.config(state=st_cbb)

        if mode == "VIEW":
            btn_them.config(state="normal"); btn_sua.config(state="normal"); btn_xoa.config(state="normal")
            btn_luu.config(state="disabled"); btn_huy.config(state="disabled")
        else:
            btn_them.config(state="disabled"); btn_sua.config(state="disabled"); btn_xoa.config(state="disabled")
            btn_luu.config(state="normal"); btn_huy.config(state="normal")

    def click_huy():
        set_state("VIEW")
        var_user.set("")
        var_pass.set("")
        var_cbb_nv.set("")
        var_vaitro.set("")
        load_combobox_nv()

    def click_them():
        click_huy()
        set_state("ADD")
        var_vaitro.set("NhanVien") # Mặc định
        entry_user.focus()

    def click_sua():
        if var_user.get():
            set_state("EDIT")
            var_pass.set("") # Xóa trắng pass để người dùng biết: Nhập mới = Đổi, Để trống = Giữ cũ
            entry_pass.focus()
            messagebox.showinfo("Hướng dẫn", "Nhập mật khẩu mới để đổi.\nĐể trống nếu muốn giữ mật khẩu cũ.")
        else:
            messagebox.showwarning("", "Chọn tài khoản cần sửa!")

    def on_click_tree(event):
        if current_mode != "VIEW": return
        item = tree.focus()
        if item:
            vals = tree.item(item, 'values')
            var_user.set(vals[0])
            
            # Tìm tên hiển thị khớp với Mã NV để set vào Combobox
            ma_nv_chon = vals[3]
            # Duyệt map ngược để tìm tên hiển thị (Vì combobox lưu tên)
            for name_display, id_val in map_nv.items():
                if id_val == ma_nv_chon:
                    var_cbb_nv.set(name_display)
                    break
            
            var_vaitro.set(vals[2])
            var_pass.set("********") # Hiển thị giả

    # --- 4. LAYOUT ---
    Label(parent_frame, text="QUẢN LÝ TÀI KHOẢN NGƯỜI DÙNG", font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=10)

    # Form
    frame_info = LabelFrame(parent_frame, text="Thông tin tài khoản", bg=BG_COLOR, font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_info.pack(fill=X, padx=20)

    def create_field(row, col, text, var, width=30, is_pass=False):
        Label(frame_info, text=text, bg=BG_COLOR).grid(row=row, column=col, sticky=W, pady=5, padx=(20 if col>0 else 0, 0))
        show_char = "*" if is_pass else ""
        w = Entry(frame_info, textvariable=var, width=width, show=show_char)
        w.grid(row=row, column=col+1, padx=5, sticky=W)
        return w

    # Dòng 1
    entry_user = create_field(0, 0, "Tên Đăng Nhập:", var_user)
    
    Label(frame_info, text="Nhân Viên:", bg=BG_COLOR).grid(row=0, column=2, sticky=W, padx=(20,0))
    cbb_nv = ttk.Combobox(frame_info, textvariable=var_cbb_nv, width=28, state="readonly")
    cbb_nv.grid(row=0, column=3, padx=5)

    # Dòng 2
    entry_pass = create_field(1, 0, "Mật Khẩu:", var_pass, is_pass=True)
    
    Label(frame_info, text="Vai Trò:", bg=BG_COLOR).grid(row=1, column=2, sticky=W, padx=(20,0))
    cbb_role = ttk.Combobox(frame_info, textvariable=var_vaitro, values=["Admin", "QuanLy", "NhanVien"], width=28, state="readonly")
    cbb_role.grid(row=1, column=3, padx=5)

    # Buttons
    frame_btn = Frame(parent_frame, bg=BG_COLOR, pady=10)
    frame_btn.pack(fill=X, padx=20)

    def mk_btn(txt, cmd, clr): return Button(frame_btn, text=txt, command=cmd, bg=clr, fg="white", width=10, relief="flat", font=("Arial", 9, "bold"))

    btn_them = mk_btn("THÊM", click_them, "#2980b9")
    btn_them.pack(side=LEFT, padx=5)
    btn_sua = mk_btn("SỬA", click_sua, "#f39c12")
    btn_sua.pack(side=LEFT, padx=5)
    btn_xoa = mk_btn("XÓA", click_xoa, "#c0392b")
    btn_xoa.pack(side=LEFT, padx=5)

    Label(frame_btn, bg=BG_COLOR, width=3).pack(side=LEFT)

    btn_luu = mk_btn("LƯU", act_luu, "#27ae60")
    btn_luu.pack(side=LEFT, padx=5)
    btn_huy = mk_btn("HỦY", click_huy, "#7f8c8d")
    btn_huy.pack(side=LEFT, padx=5)

    # Search
    frame_search = Frame(frame_btn, bg=BG_COLOR)
    frame_search.pack(side=RIGHT)

    def do_search(event=None): # Hàm này chấp nhận event để bind phím Enter
        load_data(var_search.get())
    
    def reset_search():
        var_search.set("")
        load_data()

    Button(frame_search, text="Tìm kiếm", command=do_search, bg="#34495e", fg="white").pack(side=RIGHT, padx=2)
    entry_search = Entry(frame_search, textvariable=var_search, width=25)
    entry_search.pack(side=RIGHT, padx=5)
    entry_search.bind('<Return>', do_search) # Bấm Enter để tìm ngay
    Label(frame_search, text="Tìm:", bg=BG_COLOR).pack(side=RIGHT)
    # Nút làm mới danh sách
    Button(frame_search, text="↻", command=reset_search, font=("Arial", 10, "bold"), width=3).pack(side=RIGHT, padx=5)
   
    # Table
    frame_tree = Frame(parent_frame, bg="white")
    frame_tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

    cols = ("Username", "TenNV", "VaiTro", "MaNV")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    headers = ["Tên Đăng Nhập", "Nhân Viên Sở Hữu", "Vai Trò", "Mã NV (Ẩn)"]
    widths = [150, 200, 100, 0] # Cột MaNV để width=0 để ẩn đi
    
    for c, h, w in zip(cols, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w)
        # Ẩn cột Mã NV nếu cần
        if w == 0: tree.column(c, stretch=NO)

    sb = ttk.Scrollbar(frame_tree, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set); sb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_click_tree)

    set_state("VIEW")
    load_combobox_nv()
    load_data()