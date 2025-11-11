import tkinter as tk
from tkinter import ttk, messagebox
# from tkcalendar import DateEntry # Cần uncomment nếu muốn dùng DateEntry

# Import các module CRUD để tải dữ liệu từ SQL Server
from modules.crud import khachhang_crud, nhanvien_crud, xemay_crud, hoadon_crud, chitiethoadon_crud

# --- Khai báo các biến toàn cục cho Nhân Viên ---
gender_var = None
chucvu_values = ["Quản lý", "Nhân viên", "Kế toán", "Bảo vệ"]

# =======================================================
# --- HÀM TIỆN ÍCH ---
# =======================================================
def populate_treeview(tree, data_loader):
    """Xóa dữ liệu cũ trong Treeview và chèn dữ liệu mới từ data_loader.

    Args:
        tree: ttk.Treeview widget
        data_loader: hàm trả về list of pyodbc.Row (ví dụ: khachhang_crud.load_all_data)
    """
    # Xóa tất cả dữ liệu cũ
    for item in tree.get_children():
        tree.delete(item)
    
    # Tải dữ liệu mới từ SQL Server
    rows = data_loader()
    
    # Chèn từng hàng vào Treeview
    for row in rows:
        # Chuyển pyodbc.Row thành tuple để chèn vào Treeview
        values = tuple(row)
        tree.insert("", tk.END, values=values)

def clear_main_frame():
    """Xóa tất cả các widget con trong main_frame."""
    for widget in main_frame.winfo_children():
        widget.destroy()

# --- Hàm tiện ích để tạo Frame chứa các nút chức năng ---

def create_control_buttons(parent_frame):
    """Tạo frame chứa các nút Thêm, Sửa, Xóa, Lưu, Hủy, Thoát."""
    
    # Frame chứa các nút
    button_frame = tk.Frame(parent_frame, pady=10)
    button_frame.pack(fill="x", pady=5)
    
    # Định nghĩa các nút và lệnh (hiện tại chỉ in ra thông báo)
    tk.Button(button_frame, text="Thêm", width=10, command=lambda: print("Thực hiện chức năng Thêm")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Sửa", width=10, command=lambda: print("Thực hiện chức năng Sửa")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Xóa", width=10, command=lambda: print("Thực hiện chức năng Xóa")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Lưu", width=10, command=lambda: print("Thực hiện chức năng Lưu")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Hủy", width=10, command=lambda: print("Thực hiện chức năng Hủy")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Thoát", width=10, command=main_frame.winfo_toplevel().quit).pack(side=tk.LEFT, padx=5) 

    return button_frame
# =======================================================
# --- CÁC HÀM TẠO GIAO DIỆN FORM ---
# =======================================================

### 1. FORM QUẢN LÝ NHÂN VIÊN
def create_nhanvien_frame():
    global gender_var

    clear_main_frame()
    
    # Tiêu đề chính
    lbl_title = tk.Label(main_frame, text="QUẢN LÝ NHÂN VIÊN", 
                         font=("Arial", 18, "bold"), fg="#336699")
    lbl_title.pack(pady=10)
    
    # ####### FRAME NHẬP THÔNG TIN #######
    frame_info = tk.Frame(main_frame, padx=10, pady=5, relief=tk.GROOVE, borderwidth=1)
    frame_info.pack(fill="x", padx=10, pady=10)

    gender_var = tk.StringVar(value="Nam") 
    
    # Dòng 0
    tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maso = tk.Entry(frame_info, width=15)
    entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Chức vụ").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_chucvu = ttk.Combobox(frame_info, values=chucvu_values, width=15)
    cbb_chucvu.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    cbb_chucvu.current(0) 

    # Dòng 1
    tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_holot = tk.Entry(frame_info, width=15)
    entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_ten = tk.Entry(frame_info, width=15)
    entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # Dòng 2
    tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w")
    tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w")

    tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_ngaysinh = tk.Entry(frame_info, width=15) 
    entry_ngaysinh.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    
    # ####### FRAME NÚT ĐIỀU KHIỂN #######
    create_control_buttons(main_frame) 

    # ####### BẢNG DANH SÁCH NHÂN VIÊN (Treeview) #######
    lbl_ds = tk.Label(main_frame, text="Danh sách nhân viên", font=("Arial", 15, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Định nghĩa tiêu đề cột và độ rộng
    tree.heading("maso", text="Mã số"); tree.column("maso", width=60, anchor="center")
    tree.heading("holot", text="Họ lót"); tree.column("holot", width=150, anchor="w")
    tree.heading("ten", text="Tên"); tree.column("ten", width=100, anchor="w")
    tree.heading("phai", text="Phái"); tree.column("phai", width=70, anchor="center")
    tree.heading("ngaysinh", text="Ngày sinh"); tree.column("ngaysinh", width=100, anchor="center")
    tree.heading("chucvu", text="Chức vụ"); tree.column("chucvu", width=150, anchor="w")

    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # Tải dữ liệu từ SQL Server và điền vào Treeview
    populate_treeview(tree, nhanvien_crud.load_all_data)

### 2. FORM QUẢN LÝ XE MÁY 
def create_xemay_frame():
    clear_main_frame()
    
    # Tiêu đề chính
    lbl_title = tk.Label(main_frame, text="QUẢN LÝ XE MÁY (HÀNG HOÁ)", 
                         font=("Arial", 18, "bold"), fg="#336699")
    lbl_title.pack(pady=10)
    
    # ####### FRAME NHẬP THÔNG TIN XE MÁY #######
    frame_info = tk.Frame(main_frame, padx=10, pady=5, relief=tk.GROOVE, borderwidth=1)
    frame_info.pack(fill="x", padx=10, pady=10)

    # Dòng 0: Mã Xe | Tên Xe | Loại Xe
    tk.Label(frame_info, text="Mã Xe").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maxe = tk.Entry(frame_info, width=15)
    entry_maxe.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên Xe").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tenxe = tk.Entry(frame_info, width=15)
    entry_tenxe.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Loại Xe").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    cbb_loaixe = ttk.Combobox(frame_info, values=["Xe số", "Xe ga", "Xe côn tay"], width=15)
    cbb_loaixe.grid(row=0, column=5, padx=5, pady=5, sticky="w")
    cbb_loaixe.current(0)

    # Dòng 1: Hãng Xe | Màu Sắc | Số Khung
    tk.Label(frame_info, text="Hãng Xe").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_hangxe = tk.Entry(frame_info, width=15)
    entry_hangxe.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Màu Sắc").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_mausac = tk.Entry(frame_info, width=15)
    entry_mausac.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Số Khung").grid(row=1, column=4, padx=5, pady=5, sticky="w")
    entry_sokhung = tk.Entry(frame_info, width=15)
    entry_sokhung.grid(row=1, column=5, padx=5, pady=5, sticky="w")

    # Dòng 2: Giá Nhập | Giá Bán
    tk.Label(frame_info, text="Giá Nhập").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_gianhap = tk.Entry(frame_info, width=15)
    entry_gianhap.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Giá Bán").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    entry_giaban = tk.Entry(frame_info, width=15)
    entry_giaban.grid(row=2, column=3, padx=5, pady=5, sticky="w")

    # ####### FRAME NÚT ĐIỀU KHIỂN #######
    create_control_buttons(main_frame)

    # ####### BẢNG DANH SÁCH XE MÁY (Treeview) #######
    lbl_ds = tk.Label(main_frame, text="Danh sách xe máy", font=("Arial", 15, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("maxe", "tenxe", "loaixe", "hangxe", "mausac", "gianhap", "giaban", "sokhung", "tinhtrang")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Định nghĩa tiêu đề cột và độ rộng
    tree.heading("maxe", text="Mã Xe"); tree.column("maxe", width=60, anchor="center")
    tree.heading("tenxe", text="Tên Xe"); tree.column("tenxe", width=150, anchor="w")
    tree.heading("loaixe", text="Loại Xe"); tree.column("loaixe", width=80, anchor="center")
    tree.heading("hangxe", text="Hãng Xe"); tree.column("hangxe", width=80, anchor="w")
    tree.heading("mausac", text="Màu Sắc"); tree.column("mausac", width=70, anchor="center")
    tree.heading("gianhap", text="Giá Nhập"); tree.column("gianhap", width=100, anchor="e")
    tree.heading("giaban", text="Giá Bán"); tree.column("giaban", width=100, anchor="e")
    tree.heading("sokhung", text="Số Khung"); tree.column("sokhung", width=120, anchor="center")
    tree.heading("tinhtrang", text="Tình Trạng"); tree.column("tinhtrang", width=100, anchor="center")

    tree.pack(padx=10, pady=5, fill="both", expand=True)   

    # Tải dữ liệu từ SQL Server và điền vào Treeview
    populate_treeview(tree, xemay_crud.load_all_data)   
   
### 3. FORM QUẢN LÝ KHÁCH HÀNG
def create_khachhang_frame():
    clear_main_frame()
    
    # Tiêu đề chính
    lbl_title = tk.Label(main_frame, text="QUẢN LÝ KHÁCH HÀNG", 
                         font=("Arial", 18, "bold"), fg="#336699")
    lbl_title.pack(pady=10)
    
    # ####### FRAME NHẬP THÔNG TIN KHÁCH HÀNG #######
    frame_info = tk.Frame(main_frame, padx=10, pady=5, relief=tk.GROOVE, borderwidth=1)
    frame_info.pack(fill="x", padx=10, pady=10)

    # Dòng 0: Mã KH | Tên KH
    tk.Label(frame_info, text="Mã KH").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_makh = tk.Entry(frame_info, width=15)
    entry_makh.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Tên KH").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_tenkh = tk.Entry(frame_info, width=20)
    entry_tenkh.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # Dòng 1: SDT | Địa Chỉ
    tk.Label(frame_info, text="SĐT").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_sdt = tk.Entry(frame_info, width=15)
    entry_sdt.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Địa Chỉ").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_diachi = tk.Entry(frame_info, width=20)
    entry_diachi.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # ####### FRAME NÚT ĐIỀU KHIỂN #######
    create_control_buttons(main_frame)

    # ####### BẢNG DANH SÁCH KHÁCH HÀNG (Treeview) #######
    lbl_ds = tk.Label(main_frame, text="Danh sách khách hàng", font=("Arial", 15, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("makh", "tenkh", "sdt", "diachi")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Định nghĩa tiêu đề cột và độ rộng
    tree.heading("makh", text="Mã KH"); tree.column("makh", width=80, anchor="center")
    tree.heading("tenkh", text="Tên KH"); tree.column("tenkh", width=200, anchor="w")
    tree.heading("sdt", text="SĐT"); tree.column("sdt", width=120, anchor="center")
    tree.heading("diachi", text="Địa Chỉ"); tree.column("diachi", width=350, anchor="w")

    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # Tải dữ liệu từ SQL Server và điền vào Treeview
    populate_treeview(tree, khachhang_crud.load_all_data)

### 4. FORM QUẢN LÝ HÓA ĐƠN
def create_hoadon_frame():
    clear_main_frame()
    
    # Tiêu đề chính
    lbl_title = tk.Label(main_frame, text="QUẢN LÝ HÓA ĐƠN", 
                         font=("Arial", 18, "bold"), fg="#336699")
    lbl_title.pack(pady=10)
    
    # ####### FRAME NHẬP THÔNG TIN HÓA ĐƠN #######
    frame_info = tk.Frame(main_frame, padx=10, pady=5, relief=tk.GROOVE, borderwidth=1)
    frame_info.pack(fill="x", padx=10, pady=10)

    # Dòng 0: Mã HD | Mã KH | Mã NV
    tk.Label(frame_info, text="Mã HD").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mahd = tk.Entry(frame_info, width=15)
    entry_mahd.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã KH").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_makh_hd = tk.Entry(frame_info, width=15)
    entry_makh_hd.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã NV").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    entry_manv_hd = tk.Entry(frame_info, width=15)
    entry_manv_hd.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    # Dòng 1: Ngày Lập | Tổng Tiền
    tk.Label(frame_info, text="Ngày Lập").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_ngaylap = tk.Entry(frame_info, width=15)
    entry_ngaylap.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    
    tk.Label(frame_info, text="Tổng Tiền").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_tongtien = tk.Entry(frame_info, width=15)
    entry_tongtien.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # ####### FRAME NÚT ĐIỀU KHIỂN #######
    create_control_buttons(main_frame)

    # ####### BẢNG DANH SÁCH HÓA ĐƠN (Treeview) #######
    lbl_ds = tk.Label(main_frame, text="Danh sách hóa đơn", font=("Arial", 15, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("mahd", "makh", "manv", "ngaylap", "tongtien")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Định nghĩa tiêu đề cột và độ rộng
    tree.heading("mahd", text="Mã HD"); tree.column("mahd", width=80, anchor="center")
    tree.heading("makh", text="Mã KH"); tree.column("makh", width=80, anchor="center")
    tree.heading("manv", text="Mã NV"); tree.column("manv", width=80, anchor="center")
    tree.heading("ngaylap", text="Ngày Lập"); tree.column("ngaylap", width=100, anchor="center")
    tree.heading("tongtien", text="Tổng Tiền"); tree.column("tongtien", width=120, anchor="e")

    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # Tải dữ liệu từ SQL Server và điền vào Treeview
    populate_treeview(tree, hoadon_crud.load_all_data)

### 5. FORM QUẢN LÝ CHI TIẾT HÓA ĐƠN
def create_chitiethoadon_frame():
    clear_main_frame()
    
    # Tiêu đề chính
    lbl_title = tk.Label(main_frame, text="QUẢN LÝ CHI TIẾT HÓA ĐƠN", 
                         font=("Arial", 18, "bold"), fg="#336699")
    lbl_title.pack(pady=10)
    
    # Tải dữ liệu xe máy để tạo danh sách mã xe và map giá bán
    xemay_data = xemay_crud.load_all_data()
    maxe_list = [row[0] for row in xemay_data]  # MaXe
    maxe_to_giaban = {row[0]: row[6] for row in xemay_data}  # GiaBan (index 6)
    
    # Hàm tính thành tiền
    def tinh_thanh_tien(*args):
        try:
            soluong = int(entry_soluong.get() or 0)
            dongia = float(entry_dongia.get() or 0)
            thanhtien = soluong * dongia
            entry_thanhtien.delete(0, tk.END)
            entry_thanhtien.insert(0, str(thanhtien))
        except ValueError:
            entry_thanhtien.delete(0, tk.END)
    
    # Hàm xử lý khi chọn mã xe
    def on_maxe_select(event):
        selected_maxe = cbb_maxe_ct.get()
        if selected_maxe in maxe_to_giaban:
            giaban = maxe_to_giaban[selected_maxe]
            entry_dongia.delete(0, tk.END)
            entry_dongia.insert(0, str(giaban))
            tinh_thanh_tien()  # Tính lại thành tiền
    
    # ####### FRAME NHẬP THÔNG TIN CHI TIẾT HÓA ĐƠN #######
    frame_info = tk.Frame(main_frame, padx=10, pady=5, relief=tk.GROOVE, borderwidth=1)
    frame_info.pack(fill="x", padx=10, pady=10)

    # Dòng 0: Mã HD | Mã Xe | Số Lượng
    tk.Label(frame_info, text="Mã HD").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mahd_ct = tk.Entry(frame_info, width=15)
    entry_mahd_ct.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Mã Xe").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_maxe_ct = ttk.Combobox(frame_info, values=maxe_list, width=12)
    cbb_maxe_ct.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    cbb_maxe_ct.bind("<<ComboboxSelected>>", on_maxe_select)

    tk.Label(frame_info, text="Số Lượng").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    entry_soluong = tk.Entry(frame_info, width=15)
    entry_soluong.grid(row=0, column=5, padx=5, pady=5, sticky="w")
    entry_soluong.bind("<KeyRelease>", tinh_thanh_tien)

    # Dòng 1: Đơn Giá | Thành Tiền
    tk.Label(frame_info, text="Đơn Giá").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_dongia = tk.Entry(frame_info, width=15)
    entry_dongia.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    entry_dongia.bind("<KeyRelease>", tinh_thanh_tien)
    
    tk.Label(frame_info, text="Thành Tiền").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_thanhtien = tk.Entry(frame_info, width=15, state="readonly")  # Readonly vì tính tự động
    entry_thanhtien.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # ####### FRAME NÚT ĐIỀU KHIỂN #######
    create_control_buttons(main_frame)

    # ####### BẢNG DANH SÁCH CHI TIẾT HÓA ĐƠN (Treeview) #######
    lbl_ds = tk.Label(main_frame, text="Danh sách chi tiết hóa đơn", font=("Arial", 15, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    columns = ("mahd", "maxe", "soluong", "dongia", "thanhtien")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Định nghĩa tiêu đề cột và độ rộng
    tree.heading("mahd", text="Mã HD"); tree.column("mahd", width=80, anchor="center")
    tree.heading("maxe", text="Mã Xe"); tree.column("maxe", width=80, anchor="center")
    tree.heading("soluong", text="Số Lượng"); tree.column("soluong", width=80, anchor="center")
    tree.heading("dongia", text="Đơn Giá"); tree.column("dongia", width=100, anchor="e")
    tree.heading("thanhtien", text="Thành Tiền"); tree.column("thanhtien", width=120, anchor="e")

    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # Tải dữ liệu từ SQL Server và điền vào Treeview
    populate_treeview(tree, chitiethoadon_crud.load_all_data)

# =======================================================
# --- HÀM XỬ LÝ MENU (COMMAND HANDLERS) ---
# =======================================================
def show_form_hanghoa():
    create_xemay_frame()

def show_form_nhanvien():
    create_nhanvien_frame()

def show_form_khachhang():
    create_khachhang_frame()

def show_form_hoadon():
    create_hoadon_frame()

def show_form_chitiethoadon():
    create_chitiethoadon_frame()

def show_form_chatlieu():
    clear_main_frame()
    tk.Label(main_frame, text="FORM QUẢN LÝ CHẤT LIỆU / LOẠI XE", 
             font=("Arial", 16, "bold"), fg="orange").pack(pady=50)

# =======================================================
# --- CỬA SỔ CHÍNH VÀ MENU BAR ---
# =======================================================
root = tk.Tk()
root.title("Chương trình Quản lý Cửa Hàng Xe Máy")
# Có thể thêm root.geometry("800x600") nếu muốn kích thước cố định

# -----------------------------------------------------------
# --- 1. TẠO THANH MENU CHÍNH (MENU BAR) ---
menubar = tk.Menu(root)
root.config(menu=menubar)

# -----------------------------------------------------------
# --- 2. TẠO CÁC MENU CẤP 1 (Tập tin, Danh mục, Hóa đơn...) ---
# === 2a. Menu 'Tập tin' ===
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tập tin", menu=file_menu)
file_menu.add_command(label="Đóng", command=root.quit)

# === 2b. Menu 'Danh mục' (Gọi các hàm tạo Form) ===
danhmuc_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Danh mục", menu=danhmuc_menu)

danhmuc_menu.add_command(label="Xe Máy (Hàng hoá)", command=show_form_hanghoa) 
danhmuc_menu.add_command(label="Nhân viên", command=show_form_nhanvien)
danhmuc_menu.add_command(label="Khách hàng", command=show_form_khachhang)



# === 2c. Menu 'Hoá đơn' ===
hoadon_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Hóa đơn", menu=hoadon_menu)
hoadon_menu.add_command(label="Chi tiết hóa đơn", command=show_form_chitiethoadon)
hoadon_menu.add_command(label="Xem danh sách HĐ", command=show_form_hoadon)

# -----------------------------------------------------------
# --- 3. KHU VỰC CHÍNH (FRAME CHỨA NỘI DUNG CÁC FORM) ---
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Nội dung chào mừng ban đầu
tk.Label(main_frame, text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG XE MÁY", 
         font=("Arial", 20), fg="#336699").pack(pady=50)


# ====== CHẠY VÒNG LẶP CHÍNH ======
if __name__ == "__main__":
    root.mainloop() 