from tkinter import *
from tkinter import ttk, messagebox
import utils

def create_ui(parent_frame):
    # --- 1. BIẾN DỮ LIỆU ---
    parent_frame.vars = {} 
    
    var_makh = StringVar() 
    var_hoten = StringVar()
    var_sdt = StringVar()
    var_diachi = StringVar()
    var_cccd = StringVar()
    var_search = StringVar()

    current_mode = "VIEW" 
    BG_COLOR = getattr(utils, 'MAIN_BG', 'white') 

    # --- 2. HÀM XỬ LÝ DATABASE ---
    def load_data(search_txt=None):
        for item in tree.get_children():
            tree.delete(item)
        
        try:
            conn = utils.get_connection()
            if not conn: return
            cursor = conn.cursor()
            
            sql = "SELECT MaKhachHang, HoTen, SoDienThoai, DiaChi, CCCD FROM KhachHang"
            params = []
            
            if search_txt and search_txt.strip() != "":
                sql += " WHERE MaKhachHang LIKE ? OR HoTen LIKE ? OR SoDienThoai LIKE ? OR CCCD LIKE ?"
                kw = f"%{search_txt}%"
                params = [kw, kw, kw, kw]
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            for row in rows:
                tree.insert("", END, values=(row[0], row[1], row[2], row[3], row[4]))
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def act_luu():
        # Validate
        makh = var_makh.get().strip()
        hoten = var_hoten.get().strip()
        sdt = var_sdt.get().strip()

        if not makh:
            messagebox.showwarning("Cảnh báo", "Mã khách hàng là bắt buộc!")
            return
        if not hoten:
            messagebox.showwarning("Cảnh báo", "Họ tên là bắt buộc!")
            return
        if not sdt:
            messagebox.showwarning("Cảnh báo", "Số điện thoại là bắt buộc!")
            return

        conn = utils.get_connection()
        cursor = conn.cursor()
        try:
            if current_mode == "ADD":
                # Kiểm tra trùng mã
                cursor.execute("SELECT Count(*) FROM KhachHang WHERE MaKhachHang=?", (makh,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", f"Mã khách hàng '{makh}' đã tồn tại!")
                    return

                sql = "INSERT INTO KhachHang (MaKhachHang, HoTen, SoDienThoai, DiaChi, CCCD) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(sql, (makh, hoten, sdt, var_diachi.get(), var_cccd.get()))
                messagebox.showinfo("Thành công", "Đã thêm khách hàng mới!")
                
            elif current_mode == "EDIT":
                # Không sửa Mã Khách Hàng
                sql = "UPDATE KhachHang SET HoTen=?, SoDienThoai=?, DiaChi=?, CCCD=? WHERE MaKhachHang=?"
                cursor.execute(sql, (hoten, sdt, var_diachi.get(), var_cccd.get(), makh))
                messagebox.showinfo("Thành công", "Đã cập nhật thông tin!")
            
            conn.commit()
            click_huy()
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi SQL", str(e))
        finally:
            conn.close()

    def click_xoa():
        makh = var_makh.get()
        if not makh: return
        
        if messagebox.askyesno("Xác nhận", f"Xóa khách hàng: {makh}?"):
            try:
                conn = utils.get_connection()
                try:
                    conn.execute("DELETE FROM KhachHang WHERE MaKhachHang=?", (makh,))
                    conn.commit()
                    messagebox.showinfo("Thành công", "Đã xóa khách hàng!")
                    load_data()
                    click_huy()
                except Exception as ex_sql:
                    if "REFERENCE" in str(ex_sql):
                        messagebox.showerror("Không thể xóa", "Khách hàng này đang có Hóa Đơn.\nKhông thể xóa khỏi hệ thống!")
                    else:
                        messagebox.showerror("Lỗi", str(ex_sql))
                conn.close()
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))

    # --- 3. UI CONTROLS ---
    def set_state(mode):
        nonlocal current_mode
        current_mode = mode
        
        st_entry = "normal" if mode != "VIEW" else "readonly"
        
        # Mã KH: Chỉ nhập khi ADD, Khóa khi EDIT/VIEW
        entry_makh.config(state="normal" if mode == "ADD" else "readonly") 
        
        entry_hoten.config(state=st_entry)
        entry_sdt.config(state=st_entry)
        entry_diachi.config(state=st_entry)
        entry_cccd.config(state=st_entry)

        if mode == "VIEW":
            btn_them.config(state="normal"); btn_sua.config(state="normal"); btn_xoa.config(state="normal")
            btn_luu.config(state="disabled"); btn_huy.config(state="disabled")
        else:
            btn_them.config(state="disabled"); btn_sua.config(state="disabled"); btn_xoa.config(state="disabled")
            btn_luu.config(state="normal"); btn_huy.config(state="normal")

    def click_huy():
        set_state("VIEW")
        var_makh.set(""); var_hoten.set("")
        var_sdt.set(""); var_diachi.set(""); var_cccd.set("")

    def click_them():
        click_huy()
        set_state("ADD")
        entry_makh.focus()

    def click_sua():
        if var_makh.get(): 
            set_state("EDIT")
            entry_hoten.focus()
        else: 
            messagebox.showwarning("", "Vui lòng chọn khách hàng để sửa!")

    def on_click_tree(event):
        if current_mode != "VIEW": return
        item = tree.focus()
        if item:
            vals = tree.item(item, 'values')
            var_makh.set(vals[0])
            var_hoten.set(vals[1])
            var_sdt.set(vals[2])
            var_diachi.set(vals[3])
            var_cccd.set(vals[4])

    # --- 4. LAYOUT ---
    Label(parent_frame, text="QUẢN LÝ KHÁCH HÀNG", font=("Arial", 18, "bold"), fg="#2c3e50", bg=BG_COLOR).pack(pady=10)

    # INFO FRAME
    frame_info = LabelFrame(parent_frame, text="Thông tin khách hàng", bg=BG_COLOR, font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_info.pack(fill=X, padx=20)

    def create_field(row, col, label_text, variable, width=25):
        Label(frame_info, text=label_text, bg=BG_COLOR).grid(row=row, column=col, sticky=W, pady=5, padx=(20 if col>0 else 0, 0))
        widget = Entry(frame_info, textvariable=variable, width=width)
        widget.grid(row=row, column=col+1, padx=5, sticky=W)
        return widget

    # Dòng 1
    entry_makh = create_field(0, 0, "Mã KH (*):", var_makh)
    entry_hoten = create_field(0, 2, "Họ tên (*):", var_hoten)

    # Dòng 2
    entry_sdt = create_field(1, 0, "Số ĐT (*):", var_sdt)
    entry_cccd = create_field(1, 2, "CCCD:", var_cccd)

    # Dòng 3
    Label(frame_info, text="Địa chỉ:", bg=BG_COLOR).grid(row=2, column=0, sticky=W, pady=5)
    entry_diachi = Entry(frame_info, textvariable=var_diachi, width=65)
    entry_diachi.grid(row=2, column=1, columnspan=3, padx=5, sticky=W)

    # BUTTON FRAME
    frame_btn = Frame(parent_frame, bg=BG_COLOR, pady=10)
    frame_btn.pack(fill=X, padx=20)

    def mk_btn(txt, cmd, clr): 
        return Button(frame_btn, text=txt, command=cmd, bg=clr, fg="white", width=10, relief="flat", font=("Arial", 9, "bold"))

    btn_them = mk_btn("THÊM KH", click_them, "#2980b9")
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

    # SEARCH FRAME
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
   
    # TABLE FRAME
    frame_tree = Frame(parent_frame, bg="white")
    frame_tree.pack(fill=BOTH, expand=True, padx=20, pady=10)

    cols = ("MaKH", "HoTen", "SDT", "DiaChi", "CCCD")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    headers = ["Mã KH", "Họ Tên", "SĐT", "Địa Chỉ", "CCCD"]
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