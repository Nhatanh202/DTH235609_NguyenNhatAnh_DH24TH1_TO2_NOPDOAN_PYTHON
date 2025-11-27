from tkinter import *
from tkinter import ttk, messagebox
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    # Lưu biến vào parent để không bị mất khi hàm kết thúc
    parent_frame.vars = {} 
    
    var_sokhung = StringVar()
    var_loaixe = StringVar()
    var_tenxe = StringVar()
    var_hang = StringVar()
    var_mau = StringVar()
    var_nam = StringVar()
    var_gia = StringVar()
    var_search = StringVar()

    # Biến trạng thái: "VIEW", "ADD", "EDIT"
    current_mode = "VIEW" 
    
    # Biến màu nền (Lấy từ utils hoặc mặc định trắng)
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
            
            # Câu lệnh SQL gốc
            sql = "SELECT SoKhung, LoaiXe, TenXe, HangSanXuat, MauSac, NamSanXuat, GiaBan FROM XeMay"
            params = []
            
            # --- TÌM KIẾM ĐA NĂNG ---
            if search_txt and search_txt.strip() != "":
                # Tìm theo Số khung, Tên xe, Hãng hoặc Loại xe
                sql += " WHERE SoKhung LIKE ? OR TenXe LIKE ? OR HangSanXuat LIKE ? OR LoaiXe LIKE ?"
                kw = f"%{search_txt}%"
                params = [kw, kw, kw, kw]
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                # Xử lý giá tiền (nếu NULL thì = 0)
                gia_tri = row[6] if row[6] is not None else 0
                gia_dep = "{:,.0f}".format(gia_tri)
                
                tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], row[5], gia_dep))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi Tải Dữ Liệu", str(e))

    def act_luu():
        # --- Validate dữ liệu ---
        sokhung = var_sokhung.get().strip()
        tenxe = var_tenxe.get().strip()
        
        if not sokhung:
            messagebox.showwarning("Cảnh báo", "Số khung là bắt buộc!")
            return
        if not tenxe:
            messagebox.showwarning("Cảnh báo", "Tên xe là bắt buộc!")
            return

        # Xử lý số liệu
        try: gia = float(var_gia.get().replace(",", ""))
        except: gia = 0
        
        try: nam = int(var_nam.get())
        except: nam = 2024

        conn = utils.get_connection()
        cursor = conn.cursor()
        try:
            # Gom dữ liệu (trừ số khung)
            data_values = (var_loaixe.get(), tenxe, var_hang.get(), var_mau.get(), nam, gia)

            if current_mode == "ADD":
                # Kiểm tra trùng số khung trước khi thêm
                cursor.execute("SELECT Count(*) FROM XeMay WHERE SoKhung=?", (sokhung,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", f"Số khung '{sokhung}' đã tồn tại!")
                    return
                
                # INSERT
                sql = "INSERT INTO XeMay (LoaiXe, TenXe, HangSanXuat, MauSac, NamSanXuat, GiaBan, SoKhung) VALUES (?,?,?,?,?,?,?)"
                cursor.execute(sql, data_values + (sokhung,))
                
            elif current_mode == "EDIT":
                # UPDATE: Cập nhật HẾT các trường thông tin dựa theo Số khung
                sql = """UPDATE XeMay SET LoaiXe=?, TenXe=?, HangSanXuat=?, MauSac=?, NamSanXuat=?, GiaBan=? 
                         WHERE SoKhung=?"""
                cursor.execute(sql, data_values + (sokhung,))
            
            conn.commit()
            messagebox.showinfo("Thông báo", "Lưu thành công!")
            click_huy() # Reset form
            load_data() # Load lại bảng
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def click_xoa():
        sokhung = var_sokhung.get()
        if not sokhung: return
        
        if messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa xe có số khung: {sokhung}?"):
            try:
                conn = utils.get_connection()
                # Kiểm tra ràng buộc (ví dụ đã bán trong Hóa đơn chưa)
                try:
                    conn.execute("DELETE FROM XeMay WHERE SoKhung=?", (sokhung,))
                    conn.commit()
                    messagebox.showinfo("Thành công", "Đã xóa xe!")
                    load_data()
                    click_huy()
                except Exception as ex_sql:
                    if "REFERENCE" in str(ex_sql):
                        messagebox.showerror("Không thể xóa", "Xe này đã phát sinh giao dịch (Hóa đơn/Bảo hành).\nKhông thể xóa khỏi hệ thống!")
                    else:
                        messagebox.showerror("Lỗi", str(ex_sql))
                conn.close()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # --- 3. ĐIỀU KHIỂN GIAO DIỆN ---
    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        # Trạng thái widgets
        # Khi VIEW: Chỉ đọc. Khi ADD/EDIT: Cho nhập.
        st_entry = "normal" if mode != "VIEW" else "readonly"
        st_cbb = "readonly" if mode != "VIEW" else "disabled" # Combobox ko được nhập bậy, chỉ chọn
        
        # Số khung: Chỉ cho nhập khi ADD. Khi EDIT thì khóa lại (vì là Khóa chính)
        entry_sokhung.config(state="normal" if mode == "ADD" else "readonly")
        
        # Các ô khác mở hết khi ADD/EDIT
        cbb_loaixe.config(state=st_cbb)
        cbb_hang.config(state=st_cbb)
        entry_ten.config(state=st_entry)
        entry_mau.config(state=st_entry)
        entry_nam.config(state=st_entry)
        entry_gia.config(state=st_entry)

        # Ẩn hiện nút bấm
        if mode == "VIEW":
            # Hiện nút thao tác
            btn_them.config(state="normal"); btn_sua.config(state="normal"); btn_xoa.config(state="normal")
            # Ẩn nút lưu/hủy
            btn_luu.config(state="disabled"); btn_huy.config(state="disabled")
        else:
            # Ẩn nút thao tác
            btn_them.config(state="disabled"); btn_sua.config(state="disabled"); btn_xoa.config(state="disabled")
            # Hiện nút lưu/hủy
            btn_luu.config(state="normal"); btn_huy.config(state="normal")

    def click_huy():
        set_state("VIEW")
        # Xóa trắng form
        var_sokhung.set(""); var_loaixe.set(""); var_tenxe.set("")
        var_hang.set(""); var_mau.set(""); var_nam.set(""); var_gia.set("")

    def click_them():
        click_huy() # Reset trước
        set_state("ADD")
        var_nam.set("2024") # Gợi ý năm hiện tại
        entry_sokhung.focus() # Đưa con trỏ vào ô nhập

    def click_sua():
        if var_sokhung.get(): 
            set_state("EDIT")
            entry_ten.focus() # Đưa con trỏ vào ô Tên để sửa nhanh
        else: 
            messagebox.showwarning("", "Vui lòng chọn một dòng trên bảng để sửa!")

    def on_click_tree(event):
        if current_mode != "VIEW": return # Đang nhập liệu thì cấm click lung tung
        item = tree.focus()
        if item:
            vals = tree.item(item, 'values')
            # Đổ dữ liệu lên form
            var_sokhung.set(vals[0]); var_loaixe.set(vals[1]); var_tenxe.set(vals[2])
            var_hang.set(vals[3]); var_mau.set(vals[4]); var_nam.set(vals[5])
            # Bỏ dấu phẩy ở giá tiền để sửa cho dễ
            var_gia.set(vals[6].replace(",", ""))

    # --- 4. THIẾT KẾ LAYOUT ---
    
    # === HEADER ===
    Label(parent_frame, text="QUẢN LÝ DANH SÁCH XE MÁY", font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=10)

    # === FORM NHẬP LIỆU ===
    frame_info = LabelFrame(parent_frame, text="Thông tin chi tiết", bg=BG_COLOR, font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_info.pack(fill=X, padx=20)

    # Helper tạo Label+Entry nhanh
    def create_field(row, col, label_text, variable, is_cbb=False, values=None):
        Label(frame_info, text=label_text, bg=BG_COLOR).grid(row=row, column=col, sticky=W, pady=5, padx=(20 if col>0 else 0, 0))
        if is_cbb:
            widget = ttk.Combobox(frame_info, textvariable=variable, values=values, width=22)
        else:
            widget = Entry(frame_info, textvariable=variable, width=25)
        widget.grid(row=row, column=col+1, padx=5, sticky=W)
        return widget

    # Dòng 1
    entry_sokhung = create_field(0, 0, "Số Khung (*):", var_sokhung)
    cbb_loaixe = create_field(0, 2, "Loại Xe:", var_loaixe, True, ["Xe Tay Ga", "Xe Số", "Xe Côn Tay", "Xe Điện", "Xe Phân Khối Lớn"])
    
    # Dòng 2
    entry_ten = create_field(1, 0, "Tên Xe:", var_tenxe)
    cbb_hang = create_field(1, 2, "Hãng SX:", var_hang, True, ["Honda", "Yamaha", "Suzuki", "Piaggio", "VinFast", "Kawasaki", "Ducati"])

    # Dòng 3
    entry_mau = create_field(2, 0, "Màu Sắc:", var_mau)
    entry_nam = create_field(2, 2, "Năm SX:", var_nam)

    # Dòng 4
    entry_gia = create_field(3, 0, "Giá Bán:", var_gia)
    

    # === THANH CÔNG CỤ (BUTTONS) ===
    frame_btn = Frame(parent_frame, bg=BG_COLOR, pady=10)
    frame_btn.pack(fill=X, padx=20)

    def mk_btn(txt, cmd, clr): 
        return Button(frame_btn, text=txt, command=cmd, bg=clr, fg="white", width=10, relief="flat", font=("Arial", 9, "bold"))

    # Nhóm Thao tác
    btn_them = mk_btn("THÊM MỚI", click_them, "#2980b9")
    btn_them.pack(side=LEFT, padx=5)
    btn_sua = mk_btn("SỬA", click_sua, "#f39c12")
    btn_sua.pack(side=LEFT, padx=5)
    btn_xoa = mk_btn("XÓA", click_xoa, "#c0392b")
    btn_xoa.pack(side=LEFT, padx=5)

    Label(frame_btn, bg=BG_COLOR, width=3).pack(side=LEFT) # Khoảng trắng

    # Nhóm Lưu/Hủy
    btn_luu = mk_btn("LƯU LẠI", act_luu, "#27ae60")
    btn_luu.pack(side=LEFT, padx=5)
    btn_huy = mk_btn("HỦY BỎ", click_huy, "#7f8c8d")
    btn_huy.pack(side=LEFT, padx=5)

    # === KHU VỰC TÌM KIẾM ===
    # Đặt bên phải thanh công cụ
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


    # === BẢNG DỮ LIỆU (TREEVIEW) ===
    frame_tree = Frame(parent_frame, bg="white")
    frame_tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

    cols = ("SoKhung", "LoaiXe", "TenXe", "Hang", "Mau", "Nam", "Gia")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    
    headers = ["Số Khung", "Loại Xe", "Tên Xe", "Hãng SX", "Màu", "Năm", "Giá Bán"]
    widths = [110, 100, 160, 100, 80, 60, 120]
    
    for c, h, w in zip(cols, headers, widths):
        tree.heading(c, text=h)
        tree.column(c, width=w)
        if c == "Gia": tree.column(c, anchor=E) # Căn phải giá tiền cho đẹp
    
    sb = ttk.Scrollbar(frame_tree, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set)
    sb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)
    
    tree.bind("<<TreeviewSelect>>", on_click_tree)

    # Khởi động lần đầu
    set_state("VIEW")
    load_data()