import tkinter as tk
from tkinter import ttk
from modules.constants import MAU_CHINH, MAU_PHU, MAU_NEN, MAU_BANG, MAU_CHU
from modules.tooltip import CongCuGoiY
from modules.calendar import CalendarDatePicker


def tao_thanh_ben(app):
    """Tạo thanh bên với các nút điều hướng"""
    buttons = [
        ('🏠 Trang Chủ', app.hien_thi_trang_chu, 'Về trang chủ'),
        ('👤 Nhân Viên', app.show_nhanvien, 'Quản lý nhân viên'),
        ('🛒 Khách Hàng', app.show_khachhang, 'Quản lý khách hàng'),
        ('🏍️ Xe Máy', app.show_xemay, 'Quản lý xe máy'),
        ('📄 Hóa Đơn', app.show_hoadon, 'Quản lý hóa đơn'),
        ('🚪 Đăng xuất', app.logout, 'Đăng xuất'),
        ('🔒 Đổi MK', app.show_change_password, 'Đổi mật khẩu admin'),
        ('❌ Thoát', app.root.quit, 'Thoát ứng dụng')
    ]
    for text, cmd, tip in buttons:
        btn = tk.Button(app.khung_thanh_ben, text=text, command=cmd, bg=MAU_CHINH, fg='white', font=('Segoe UI', 10), relief='flat', bd=0, padx=10, pady=10, anchor='w')
        btn.pack(fill=tk.X, padx=5, pady=2)
        CongCuGoiY(btn, tip)
        # Hover effect
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=MAU_PHU))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=MAU_CHINH))


def tao_form(panel, ten_bang, cot, headings, nv_options, kh_options, xm_options, app):
    """Tạo form nhập liệu"""
    form = tk.Frame(panel, bg=MAU_BANG)
    form.pack(fill=tk.X, pady=(10, 6), padx=10)
    app.form_entries = {}
    for i, col in enumerate(cot):
        lbl = tk.Label(form, text=headings[i], bg=MAU_BANG, fg=MAU_CHU)
        lbl.grid(row=0, column=i, padx=8, pady=2, sticky='w')
        ent = tao_widget(form, ten_bang, col, nv_options, kh_options, xm_options, i, app)
        app.form_entries[col] = ent
        form.columnconfigure(i, weight=1)


def tao_widget(form, ten_bang, col, nv_options, kh_options, xm_options, i, app):
    """Tạo widget phù hợp cho từng trường"""
    if col.lower() == 'phai' or col == 'Phai':
        ent = ttk.Combobox(form, values=['Nam', 'Nữ', 'Khác'], state='readonly', width=8)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
    elif col.lower() == 'ngaysinh' or col == 'NgaySinh' or col.lower() == 'ngaylap' or col == 'NgayLap':
        dp = CalendarDatePicker(form)
        dp.frame.grid(row=1, column=i, padx=8, pady=2, sticky='w')
        ent = dp
    elif col.lower() == 'hangxe' or col == 'HangXe':
        ent = ttk.Combobox(form, values=['Honda', 'Yamaha', 'Suzuki', 'Kymco', 'Sym', 'VinFast', 'YaDea', 'DatBike', 'Khác...'], state='readonly', width=10)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
    elif col.lower() == 'loaixe' or col == 'LoaiXe':
        ent = ttk.Combobox(form, values=['Xe số', 'Xe ga', 'Xe côn', 'Xe điện'], state='readonly', width=8)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
    elif ten_bang == 'HoaDon' and col == 'MaNV':
        ent = ttk.Combobox(form, values=nv_options, state='readonly', width=15)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
    elif ten_bang == 'HoaDon' and col == 'MaKH':
        ent = ttk.Combobox(form, values=kh_options, state='readonly', width=15)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
    elif ten_bang == 'HoaDon' and col == 'MaXe':
        ent = ttk.Combobox(form, values=xm_options, state='readonly', width=20)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
        ent.bind('<<ComboboxSelected>>', lambda e: app._on_select_xm())
    elif ten_bang == 'HoaDon' and col == 'SoLuong':
        ent = tk.Entry(form, bg='white', fg=MAU_CHU)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
        ent.bind('<KeyRelease>', lambda e: app._calculate_total())
    elif ten_bang == 'HoaDon' and col == 'MaHD':
        ent = ttk.Entry(form, state='readonly')
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
    else:
        ent = tk.Entry(form, bg='white', fg=MAU_CHU)
        ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
    return ent


def tao_cac_nut(panel, ten_bang, cot, app):
    """Tạo các nút CRUD"""
    ttk.Separator(panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=(0, 4))
    btn_frame = tk.Frame(panel, bg=MAU_BANG)
    btn_frame.pack(fill=tk.X, pady=(4, 10), padx=10)
    btn_add = ttk.Button(btn_frame, text='Thêm', width=10, style='Primary.TButton', command=lambda: app.khi_them(ten_bang, cot))
    btn_add.pack(side=tk.LEFT, padx=6)
    CongCuGoiY(btn_add, 'Thêm bản ghi mới')
    btn_edit = ttk.Button(btn_frame, text='Sửa', width=10, style='Primary.TButton', command=lambda: app.khi_sua(ten_bang, cot))
    btn_edit.pack(side=tk.LEFT, padx=6)
    CongCuGoiY(btn_edit, 'Cập nhật bản ghi đã chọn')
    btn_delete = ttk.Button(btn_frame, text='Xóa', width=10, style='Primary.TButton', command=lambda: app.khi_xoa(ten_bang, cot))
    btn_delete.pack(side=tk.LEFT, padx=6)
    CongCuGoiY(btn_delete, 'Xóa bản ghi đã chọn')
    tk.Label(btn_frame, text='Tìm kiếm:', bg=MAU_BANG, fg=MAU_CHU).pack(side=tk.LEFT, padx=(20,4))
    truong_tim = ttk.Entry(btn_frame)
    truong_tim.pack(side=tk.LEFT, padx=4)
    btn_search = ttk.Button(btn_frame, text='Tìm', width=8, command=lambda: app.khi_tim_kiem(ten_bang, cot, truong_tim.get().strip()))
    btn_search.pack(side=tk.LEFT, padx=6)
    CongCuGoiY(btn_search, 'Tìm kiếm bản ghi')
    btn_refresh = ttk.Button(btn_frame, text='Tải lại', width=8, command=lambda: app.lam_moi_bang(ten_bang, cot))
    btn_refresh.pack(side=tk.RIGHT, padx=6)
    CongCuGoiY(btn_refresh, 'Tải lại dữ liệu')


def tao_bang(panel, ten_bang, cot, headings, display_name, app):
    """Tạo bảng hiển thị dữ liệu"""
    ttk.Separator(panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=(10, 4))
    tk.Label(panel, text=f'Danh sách {display_name}', font=('Arial', 16, 'bold'), bg=MAU_NEN, fg=MAU_CHINH).pack(pady=(10, 4))
    frame = tk.Frame(panel)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
    tree = ttk.Treeview(frame, columns=cot, show='headings', height=15)
    for col, hd in zip(cot, headings):
        tree.heading(col, text=hd)
        tree.column(col, width=120, anchor=tk.CENTER)
    vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=vsb.set)
    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    tree.pack(fill=tk.BOTH, expand=True)
    app.current_table = ten_bang
    app.current_columns = cot
    app.current_tree = tree
    app.lam_moi_bang(ten_bang, cot)
    tree.bind('<<TreeviewSelect>>', lambda e: app._populate_form(tree.item(tree.selection()[0], 'values') if tree.selection() else ()))
    # app.set_status(f'Xem: {ten_bang}')