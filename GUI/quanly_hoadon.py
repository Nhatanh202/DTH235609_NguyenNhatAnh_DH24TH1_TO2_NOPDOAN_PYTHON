from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime 
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    parent_frame.vars = {}
    
    var_mahd = StringVar()
    var_ngayban = StringVar()
    var_tongtien = StringVar()
    var_ghichu = StringVar()
    var_search = StringVar()
    
    var_cbb_khach = StringVar()
    var_cbb_xe = StringVar()
    var_cbb_nv = StringVar()
    
    # Biến lưu số khung gốc để xử lý khi Sửa
    var_sokhung_goc = StringVar() 

    # Map dữ liệu
    map_khach = {} 
    map_nv = {}          
    map_xe = {}     # Tên hiển thị -> Số khung
    map_gia_xe = {} # Số khung -> Giá bán (Lấy từ bảng XeMay)

    current_mode = "VIEW"
    BG_COLOR = getattr(utils, 'MAIN_BG', 'white')

    # --- 2. HÀM DATABASE ---
    def load_combobox_data():
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()

            # 1. Nhân Viên
            cursor.execute("SELECT MaNhanVien, HoVaTen FROM NhanVien WHERE TrangThai=1")
            map_nv.clear(); cbb_nv['values'] = []; list_nv = []
            for row in cursor.fetchall():
                display = f"{row[1]} ({row[0]})"
                map_nv[display] = row[0]
                list_nv.append(display)
            cbb_nv['values'] = list_nv

            # 2. Khách Hàng
            cursor.execute("SELECT MaKhachHang, HoTen, SoDienThoai FROM KhachHang")
            map_khach.clear(); cbb_khach['values'] = []; list_kh = []
            for row in cursor.fetchall():
                display = f"{row[1]} - {row[2]}"
                map_khach[display] = row[0]
                list_kh.append(display)
            cbb_khach['values'] = list_kh

            # 3. Xe (Chỉ lấy xe chưa bán)
            # Lấy Giá Bán để lưu vào map_gia_xe
            sql_xe = "SELECT SoKhung, TenXe, MauSac, GiaBan FROM XeMay WHERE SoKhung NOT IN (SELECT SoKhung FROM HoaDon)"
            cursor.execute(sql_xe)
            map_xe.clear(); map_gia_xe.clear(); cbb_xe['values'] = []; list_xe = []
            for row in cursor.fetchall():
                display = f"{row[1]} ({row[2]}) - {row[0]}" 
                map_xe[display] = row[0]    
                
                # Lưu giá gốc (ép kiểu float để an toàn)
                gia_goc = float(row[3]) if row[3] else 0.0
                map_gia_xe[row[0]] = gia_goc 
                
                list_xe.append(display)
            cbb_xe['values'] = list_xe
            
            conn.close()
        except Exception as e:
            print(f"Lỗi load combo: {e}")

    def load_data(search_txt=None):
        for item in tree.get_children(): tree.delete(item)
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()
            
            # Lấy thêm MauSac để hiển thị khớp với combobox
            sql = """
                SELECT hd.MaHoaDon, nv.HoVaTen, kh.HoTen, xm.TenXe, xm.SoKhung, hd.NgayBan, hd.TongTien, hd.GhiChu, xm.MauSac
                FROM HoaDon hd
                JOIN NhanVien nv ON hd.MaNhanVien = nv.MaNhanVien
                JOIN KhachHang kh ON hd.MaKhachHang = kh.MaKhachHang
                JOIN XeMay xm ON hd.SoKhung = xm.SoKhung
            """
            params = []
            if search_txt and search_txt.strip() != "":
                sql += " WHERE hd.MaHoaDon LIKE ? OR kh.HoTen LIKE ? OR nv.HoVaTen LIKE ?"
                kw = f"%{search_txt}%"
                params = [kw, kw, kw]
                
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            for row in rows:
                ngay = ""
                if row[5]:
                    if isinstance(row[5], str): ngay = row[5]
                    else: ngay = row[5].strftime("%d/%m/%Y")
                
                tien = "{:,.0f}".format(row[6]) if row[6] else "0"
                # Indices: 0:MaHD, 1:NV, 2:KH, 3:TenXe, 4:SoKhung, 5:Ngay, 6:Tien, 7:GhiChu, 8:Mau
                tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4], ngay, tien, row[7], row[8]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def act_luu():
        txt_hd = var_mahd.get().strip()
        txt_nv = var_cbb_nv.get()
        txt_kh = var_cbb_khach.get()
        txt_xe = var_cbb_xe.get()
        txt_ngay = var_ngayban.get()

        # 1. Validate
        if not txt_hd: return messagebox.showwarning("Thiếu tin", "Vui lòng nhập Mã Hóa Đơn!")
        if not txt_nv or not txt_kh: return messagebox.showwarning("Thiếu tin", "Vui lòng chọn Nhân viên và Khách hàng!")

        # 2. Ngày
        try:
            ngay_obj = datetime.strptime(txt_ngay, "%d/%m/%Y")
            ngay_sql = ngay_obj.strftime("%Y-%m-%d")
        except: return messagebox.showerror("Lỗi ngày", "Ngày sai định dạng (dd/mm/yyyy)")

        conn = utils.get_connection()
        cursor = conn.cursor()
        
        try:
            # 3. Map ID
            try:
                ma_nv = map_nv.get(txt_nv)
                ma_kh = map_khach.get(txt_kh)
                # Nếu người dùng không chọn từ list mà gõ tay -> Lỗi
                if not ma_nv or not ma_kh: raise ValueError
            except:
                return messagebox.showwarning("Chọn lại", "Vui lòng chọn Nhân viên và Khách hàng từ danh sách!")

            # 4. Xử lý Xe & Tiền
            so_khung_final = ""
            
            if txt_xe in map_xe:
                # Chọn xe mới từ danh sách
                so_khung_final = map_xe[txt_xe]
            elif current_mode == "EDIT" and var_sokhung_goc.get() != "":
                # Sửa nhưng giữ nguyên xe cũ
                so_khung_final = var_sokhung_goc.get()
            else:
                return messagebox.showwarning("Thiếu tin", "Vui lòng chọn Xe!")

            # Lấy tiền
            try: tong_tien = float(var_tongtien.get().replace(",", ""))
            except: tong_tien = 0

            # 5. SQL
            if current_mode == "ADD":
                cursor.execute("SELECT Count(*) FROM HoaDon WHERE MaHoaDon=?", (txt_hd,))
                if cursor.fetchone()[0] > 0:
                    return messagebox.showerror("Trùng mã", "Mã hóa đơn này đã tồn tại!")

                sql = "INSERT INTO HoaDon (MaHoaDon, MaNhanVien, MaKhachHang, SoKhung, TongTien, NgayBan, GhiChu) VALUES (?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql, (txt_hd, ma_nv, ma_kh, so_khung_final, tong_tien, ngay_sql, var_ghichu.get()))
                messagebox.showinfo("Thành công", "Đã thêm hóa đơn!")

            elif current_mode == "EDIT":
                sql = "UPDATE HoaDon SET MaNhanVien=?, MaKhachHang=?, SoKhung=?, TongTien=?, NgayBan=?, GhiChu=? WHERE MaHoaDon=?"
                cursor.execute(sql, (ma_nv, ma_kh, so_khung_final, tong_tien, ngay_sql, var_ghichu.get(), txt_hd))
                messagebox.showinfo("Thành công", "Đã cập nhật hóa đơn!")

            conn.commit()
            click_huy()          
            load_combobox_data() 
            load_data()          
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def click_xoa():
        ma_hd = var_mahd.get()
        if not ma_hd: return
        if messagebox.askyesno("Cảnh báo", f"Xóa hóa đơn {ma_hd}?"):
            try:
                conn = utils.get_connection()
                conn.execute("DELETE FROM HoaDon WHERE MaHoaDon=?", (ma_hd,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa.")
                click_huy()
                load_combobox_data() 
                load_data()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # --- 3. UI CONTROL ---
    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        st_entry = "normal" if mode != "VIEW" else "readonly"
        st_cbb = "readonly" if mode != "VIEW" else "disabled"
        
        entry_mahd.config(state="normal" if mode == "ADD" else "readonly")
        
        cbb_nv.config(state=st_cbb)
        cbb_khach.config(state=st_cbb)
        
        # Cho phép chọn xe cả khi ADD và EDIT
        cbb_xe.config(state="readonly" if mode in ["ADD", "EDIT"] else "disabled")
        
        entry_ngay.config(state=st_entry)
        entry_ghi.config(state=st_entry)
        
        entry_tien.config(state="readonly") 

        if mode == "VIEW":
            btn_them.config(state="normal"); btn_sua.config(state="normal"); btn_xoa.config(state="normal")
            btn_luu.config(state="disabled"); btn_huy.config(state="disabled")
        else:
            btn_them.config(state="disabled"); btn_sua.config(state="disabled"); btn_xoa.config(state="disabled")
            btn_luu.config(state="normal"); btn_huy.config(state="normal")

    def click_huy():
        set_state("VIEW")
        var_mahd.set(""); var_cbb_nv.set(""); var_cbb_khach.set("")
        var_cbb_xe.set(""); var_tongtien.set(""); var_ngayban.set(""); var_ghichu.set("")
        var_sokhung_goc.set("")
        load_combobox_data() 

    def click_them():
        click_huy()
        set_state("ADD")
        entry_mahd.focus()
        var_ngayban.set(datetime.now().strftime("%d/%m/%Y"))

    def click_sua():
        if var_mahd.get():
            set_state("EDIT")
        else:
            messagebox.showwarning("", "Chọn hóa đơn cần sửa!")

    def on_xe_selected(event):
        # --- LOGIC CẬP NHẬT GIÁ ---
        txt_xe = var_cbb_xe.get()
        if txt_xe in map_xe:
            so_khung = map_xe[txt_xe]
            
            # Lấy đúng giá gốc từ map (đã load ở trên)
            gia_chuan = map_gia_xe.get(so_khung, 0)
            
            # Hiển thị giá chuẩn (Không nhân chia gì thêm)
            var_tongtien.set("{:,.0f}".format(gia_chuan))

    def on_click_tree(event):
        if current_mode != "VIEW": return
        item = tree.focus()
        if item:
            vals = tree.item(item, 'values')
            var_mahd.set(vals[0])
            var_cbb_nv.set(vals[1])
            var_cbb_khach.set(vals[2])
            
            # Hiển thị xe lên Combobox
            xe_display = f"{vals[3]} ({vals[8]}) - {vals[4]}"
            var_cbb_xe.set(xe_display)
            
            # Lưu lại số khung gốc
            var_sokhung_goc.set(vals[4])

            var_ngayban.set(vals[5])
            var_tongtien.set(vals[6])
            var_ghichu.set(vals[7])

    # --- 4. LAYOUT ---
    Label(parent_frame, text="QUẢN LÝ HÓA ĐƠN", font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=10)

    frame_info = LabelFrame(parent_frame, text="Thông tin chi tiết", bg=BG_COLOR, font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_info.pack(fill=X, padx=20)

    def create_field(row, col, text, var, width=30, state="normal", is_cbb=False):
        Label(frame_info, text=text, bg=BG_COLOR).grid(row=row, column=col, sticky=W, pady=5, padx=(20 if col>0 else 0, 0))
        if is_cbb:
            w = ttk.Combobox(frame_info, textvariable=var, width=width, state="readonly")
        else:
            w = Entry(frame_info, textvariable=var, width=width+2, state=state)
        w.grid(row=row, column=col+1, padx=5, sticky=W)
        return w

    entry_mahd = create_field(0, 0, "Mã HĐ (*):", var_mahd)
    cbb_nv = create_field(0, 2, "Nhân Viên:", var_cbb_nv, is_cbb=True)

    cbb_khach = create_field(1, 0, "Khách Hàng:", var_cbb_khach, is_cbb=True)
    entry_ngay = create_field(1, 2, "Ngày Bán:", var_ngayban)
    Label(frame_info, text="(dd/mm/yyyy)", bg=BG_COLOR, font=("Arial", 8)).grid(row=1, column=4, sticky=W)

    cbb_xe = create_field(2, 0, "Chọn Xe:", var_cbb_xe, is_cbb=True)
    cbb_xe.bind("<<ComboboxSelected>>", on_xe_selected) # Gắn sự kiện chọn xe
    
    entry_tien = create_field(2, 2, "Tổng Tiền:", var_tongtien, state="readonly")
    entry_tien.config(fg="red", font=("Arial", 9, "bold"))

    Label(frame_info, text="Ghi Chú:", bg=BG_COLOR).grid(row=3, column=0, sticky=W, pady=5)
    entry_ghi = Entry(frame_info, textvariable=var_ghichu, width=85)
    entry_ghi.grid(row=3, column=1, columnspan=3, padx=5, sticky=W)

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

    frame_tree = Frame(parent_frame, bg="white")
    frame_tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

    cols = ("MaHD", "NV", "KH", "Xe", "Khung", "Ngay", "Tien", "GhiChu", "Mau")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    headers = ["Mã HĐ", "Nhân Viên", "Khách Hàng", "Tên Xe", "Số Khung", "Ngày Bán", "Tổng Tiền", "Ghi Chú"]
    widths = [60, 120, 120, 100, 100, 80, 100, 150, 0]
    for c, h, w in zip(cols, headers, widths): tree.heading(c, text=h); tree.column(c, width=w)
    
    sb = ttk.Scrollbar(frame_tree, orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=sb.set); sb.pack(side=RIGHT, fill=Y)
    tree.pack(fill=BOTH, expand=True)
    tree.bind("<<TreeviewSelect>>", on_click_tree)

    set_state("VIEW")
    load_combobox_data()
    load_data()