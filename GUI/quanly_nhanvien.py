from tkinter import *
from tkinter import ttk, messagebox
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    parent_frame.vars = {} 
    
    var_manv = StringVar()
    var_hoten = StringVar()
    var_sdt = StringVar()
    var_diachi = StringVar()
    var_trangthai = StringVar() # Hiển thị: "Đang làm việc" / "Đã nghỉ"
    var_search = StringVar()

    # Biến trạng thái: "VIEW", "ADD", "EDIT"
    current_mode = "VIEW" 
    
    # Màu nền
    BG_COLOR = getattr(utils, 'MAIN_BG', 'white') 

    # --- 2. HÀM XỬ LÝ DATABASE ---
    def load_data(search_txt=None):
        # Xóa bảng cũ
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()
            
            sql = "SELECT MaNhanVien, HoVaTen, SoDienThoai, DiaChi, TrangThai FROM NhanVien"
            params = []
            
            if search_txt and search_txt.strip() != "":
                sql += " WHERE MaNhanVien LIKE ? OR HoVaTen LIKE ? OR SoDienThoai LIKE ?"
                kw = f"%{search_txt}%"
                params = [kw, kw, kw]
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                # Xử lý hiển thị trạng thái (DB lưu 1/0 -> Giao diện hiện chữ)
                trang_thai_text = "Đang làm việc" if row[4] == 1 else "Đã nghỉ việc"
                
                tree.insert("", END, values=(row[0], row[1], row[2], row[3], trang_thai_text))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu", str(e))

    def act_luu():
        # --- Validate ---
        manv = var_manv.get().strip()
        hoten = var_hoten.get().strip()
        
        if not manv:
            messagebox.showwarning("Cảnh báo", "Mã nhân viên là bắt buộc!")
            return
        if not hoten:
            messagebox.showwarning("Cảnh báo", "Họ tên là bắt buộc!")
            return

        # Chuyển đổi trạng thái từ chữ -> số để lưu vào DB
        status_val = 1 if var_trangthai.get() == "Đang làm việc" else 0

        conn = utils.get_connection()
        cursor = conn.cursor()
        try:
            if current_mode == "ADD":
                # Check trùng
                cursor.execute("SELECT Count(*) FROM NhanVien WHERE MaNhanVien=?", (manv,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", f"Mã NV '{manv}' đã tồn tại!")
                    return
                
                sql = "INSERT INTO NhanVien (MaNhanVien, HoVaTen, SoDienThoai, DiaChi, TrangThai) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(sql, (manv, hoten, var_sdt.get(), var_diachi.get(), status_val))
                
            elif current_mode == "EDIT":
                sql = "UPDATE NhanVien SET HoVaTen=?, SoDienThoai=?, DiaChi=?, TrangThai=? WHERE MaNhanVien=?"
                cursor.execute(sql, (hoten, var_sdt.get(), var_diachi.get(), status_val, manv))
            
            conn.commit()
            messagebox.showinfo("Thông báo", "Lưu thành công!")
            click_huy()
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def click_xoa():
        manv = var_manv.get()
        if not manv: return
        
        if messagebox.askyesno("Xác nhận", f"Xóa nhân viên: {manv}?"):
            try:
                conn = utils.get_connection()
                try:
                    conn.execute("DELETE FROM NhanVien WHERE MaNhanVien=?", (manv,))
                    conn.commit()
                    messagebox.showinfo("Thành công", "Đã xóa nhân viên!")
                    load_data()
                    click_huy()
                except Exception as ex_sql:
                    if "REFERENCE" in str(ex_sql):
                        messagebox.showerror("Không thể xóa", "Nhân viên này đã lập Hóa đơn hoặc có tài khoản.\nBạn nên chuyển trạng thái sang 'Đã nghỉ việc' thay vì xóa!")
                    else:
                        messagebox.showerror("Lỗi", str(ex_sql))
                conn.close()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # --- 3. ĐIỀU KHIỂN GIAO DIỆN ---
    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        st_entry = "normal" if mode != "VIEW" else "readonly"
        st_cbb = "readonly" if mode != "VIEW" else "disabled"
        
        # Mã NV: Chỉ nhập khi ADD
        entry_manv.config(state="normal" if mode == "ADD" else "readonly")
        
        entry_hoten.config(state=st_entry)
        entry_sdt.config(state=st_entry)
        entry_diachi.config(state=st_entry)
        cbb_trangthai.config(state=st_cbb)

        if mode == "VIEW":
            btn_them.config(state="normal"); btn_sua.config(state="normal"); btn_xoa.config(state="normal")
            btn_luu.config(state="disabled"); btn_huy.config(state="disabled")
        else:
            btn_them.config(state="disabled"); btn_sua.config(state="disabled"); btn_xoa.config(state="disabled")
            btn_luu.config(state="normal"); btn_huy.config(state="normal")

    def click_huy():
        set_state("VIEW")
        var_manv.set(""); var_hoten.set(""); var_sdt.set("")
        var_diachi.set(""); var_trangthai.set("")

    def click_them():
        click_huy()
        set_state("ADD")
        var_trangthai.set("Đang làm việc") # Mặc định
        entry_manv.focus()

    def click_sua():
        if var_manv.get(): 
            set_state("EDIT")
            entry_hoten.focus()
        else: 
            messagebox.showwarning("", "Vui lòng chọn nhân viên để sửa!")

    def on_click_tree(event):
        if current_mode != "VIEW": return
        item = tree.focus()
        if item:
            vals = tree.item(item, 'values')
            var_manv.set(vals[0])
            var_hoten.set(vals[1])
            var_sdt.set(vals[2])
            var_diachi.set(vals[3])
            var_trangthai.set(vals[4])

    # --- 4. THIẾT KẾ LAYOUT ---
    Label(parent_frame, text="QUẢN LÝ NHÂN SỰ", font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=10)

    # FORM
    frame_info = LabelFrame(parent_frame, text="Thông tin nhân viên", bg=BG_COLOR, font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_info.pack(fill=X, padx=20)

    def create_field(row, col, label_text, variable, width=25):
        Label(frame_info, text=label_text, bg=BG_COLOR).grid(row=row, column=col, sticky=W, pady=5, padx=(20 if col>0 else 0, 0))
        widget = Entry(frame_info, textvariable=variable, width=width)
        widget.grid(row=row, column=col+1, padx=5, sticky=W)
        return widget

    # Dòng 1
    entry_manv = create_field(0, 0, "Mã NV (*):", var_manv)
    entry_hoten = create_field(0, 2, "Họ và Tên (*):", var_hoten)

    # Dòng 2
    entry_sdt = create_field(1, 0, "Số điện thoại:", var_sdt)
    entry_diachi = create_field(1, 2, "Địa chỉ:", var_diachi)

    # Dòng 3: Trạng thái (Combobox)
    Label(frame_info, text="Trạng thái:", bg=BG_COLOR).grid(row=2, column=0, sticky=W, pady=5)
    cbb_trangthai = ttk.Combobox(frame_info, textvariable=var_trangthai, values=["Đang làm việc", "Đã nghỉ việc"], width=22)
    cbb_trangthai.grid(row=2, column=1, padx=5, sticky=W)

    # BUTTONS
    frame_btn = Frame(parent_frame, bg=BG_COLOR, pady=10)
    frame_btn.pack(fill=X, padx=20)

    def mk_btn(txt, cmd, clr): 
        return Button(frame_btn, text=txt, command=cmd, bg=clr, fg="white", width=10, relief="flat", font=("Arial", 9, "bold"))

    btn_them = mk_btn("THÊM NV", click_them, "#2980b9")
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

    # SEARCH
    frame_search = Frame(frame_btn, bg=BG_COLOR)
    frame_search.pack(side=RIGHT)
    
    def do_search(event=None): load_data(var_search.get())
    def reset_search(): var_search.set(""); load_data()

    Button(frame_search, text="Tìm kiếm", command=do_search, bg="#34495e", fg="white").pack(side=RIGHT, padx=2)
    entry_search = Entry(frame_search, textvariable=var_search, width=25)
    entry_search.pack(side=RIGHT, padx=5)
    entry_search.bind('<Return>', do_search) # Bấm Enter để tìm ngay
    Label(frame_search, text="Tìm:", bg=BG_COLOR).pack(side=RIGHT)
    # Nút làm mới danh sách
    Button(frame_search, text="↻", command=reset_search, font=("Arial", 10, "bold"), width=3).pack(side=RIGHT, padx=5)

    # TABLE
    frame_tree = Frame(parent_frame, bg="white")
    frame_tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

    cols = ("MaNV", "HoTen", "SDT", "DiaChi", "TrangThai")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    headers = ["Mã NV", "Họ và Tên", "Số ĐT", "Địa Chỉ", "Trạng Thái"]
    widths = [80, 150, 100, 200, 100]
    
    for c, h, w in zip(cols, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w)
    
    sb = ttk.Scrollbar(frame_tree, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set); sb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_click_tree)

    set_state("VIEW")
    load_data()
