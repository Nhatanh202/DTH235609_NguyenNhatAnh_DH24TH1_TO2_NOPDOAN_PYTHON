import tkinter as tk
from tkinter import ttk, messagebox
from modules.auth import check_login
from modules.data import load_data
from modules.calendar import CalendarDatePicker
from modules.crud import execute_write, insert_record, update_record, delete_record, search_records, get_quantity, insert_hoa_don, generate_mahd
from modules.constants import MAU_CHINH, MAU_PHU, MAU_NEN, MAU_BANG, MAU_CHU, TABLE_CONFIGS
from modules.tooltip import CongCuGoiY
from modules.login import tao_cua_so_dang_nhap
from modules.ui_components import tao_thanh_ben, tao_form, tao_cac_nut, tao_bang
from modules.crud_handlers import lam_moi_bang, khi_them, khi_sua, khi_xoa, khi_tim_kiem, validate_data, check_exists


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Quản lý Cửa hàng Xe Máy')
        self.root.geometry('1000x650')
        self.root.state('zoomed')

        # apply theme to root
        try:
            self.root.configure(bg=MAU_NEN)
        except Exception:
            pass

        # ttk styling
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        # Treeview styling with striped rows
        try:
            self.style.configure('Treeview', background=MAU_BANG, fieldbackground=MAU_BANG, foreground=MAU_CHU)
            self.style.configure('Treeview.Heading', background=MAU_CHINH, foreground='white', font=('Segoe UI', 10, 'bold'))
            self.style.map('Treeview', background=[('selected', MAU_CHINH)])
            self.style.configure('evenrow', background=MAU_BANG)
            self.style.configure('oddrow', background='#f5f5f5')
        except Exception:
            pass
        # Primary button style
        try:
            self.style.configure('Primary.TButton', background=MAU_CHINH, foreground='white')
            self.style.map('Primary.TButton', background=[('active', MAU_PHU)])
        except Exception:
            pass
        # Toolbar button style
        try:
            self.style.configure('Toolbar.TButton', background=MAU_CHINH, foreground='white', font=('Segoe UI', 9))
            self.style.map('Toolbar.TButton', background=[('active', MAU_PHU)])
        except Exception:
            pass
        # LabelFrame style for group box
        try:
            self.style.configure('TLabelFrame', background=MAU_BANG, borderwidth=1, relief='flat')
            self.style.configure('TLabelFrame.Label', background=MAU_BANG, foreground=MAU_CHINH, font=('Segoe UI', 10, 'bold'))
        except Exception:
            pass

        # session
        self.current_user = None
        self.is_admin = False

        # frames: sidebar on left and content on right
        self.khung_thanh_ben = tk.Frame(self.root, width=180, bg=MAU_CHINH)
        self.khung_thanh_ben.pack(side=tk.LEFT, fill=tk.Y)
        self.khung_thanh_ben.pack_propagate(False)  # Keep width
        self.content_frame = tk.Frame(self.root, bg=MAU_NEN)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # table configs
        self.table_configs = TABLE_CONFIGS

        self._build_sidebar()
        self.show_home()

    def _build_tabs(self):
        tabs = [
            ('Nhân Viên', 'NhanVien'),
            ('Khách Hàng', 'KhachHang'),
            ('Xe Máy', 'XeMay'),
            (' Hóa Đơn', 'HoaDon')
        ]
        for text, name in tabs:
            frame = tk.Frame(self.notebook, bg=MAU_NEN)
            self.tab_frames[name] = frame
            self.notebook.add(frame, text=text)

    def _build_sidebar(self):
        tao_thanh_ben(self)

    def clear_content(self, parent=None):
        if parent is None:
            parent = self.content_frame
        for w in parent.winfo_children():
            w.destroy()

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_frame, text='CHÀO MỪNG ĐẾN VỚI HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY',
                 font=('Arial', 18, 'bold'), bg=MAU_NEN, fg=MAU_CHINH).pack(pady=40)
        tk.Label(self.content_frame, text='Sử dụng thanh bên để chuyển giữa các danh sách', font=('Arial', 12), bg=MAU_NEN, fg=MAU_CHU).pack()

    def hien_thi_trang_chu(self):
        self.show_home()

    def create_table_frame(self, table_name, columns, headings):
        self.clear_content()

        display_name = {'KhachHang': 'Khách Hàng', 'NhanVien': 'Nhân Viên', 'XeMay': 'Xe Máy', 'HoaDon': 'Hóa Đơn'}.get(table_name, table_name)

        # Load options for HoaDon comboboxes
        nv_options = []
        kh_options = []
        xm_options = []
        if table_name == 'HoaDon':
            nv_options = [f"{row[0]} - {row[1]} {row[2]}" for row in load_data('NhanVien')]
            kh_options = [f"{row[0]} - {row[1]}" for row in load_data('KhachHang')]
            xm_options = [f"{row[0]} - {row[1]} - {row[5]}" for row in load_data('XeMay')]

        # panel for form and buttons
        panel = tk.Frame(self.content_frame, bg=MAU_BANG, bd=1, relief='flat')
        panel.pack(fill=tk.X, padx=10, pady=(4, 10))

        self._create_form(panel, table_name, columns, headings, nv_options, kh_options, xm_options)
        self._create_buttons(panel, table_name, columns)
        self._create_tree(table_name, columns, headings, display_name)

    def _create_form(self, panel, table_name, columns, headings, nv_options, kh_options, xm_options):
        form = tk.Frame(panel, bg=MAU_BANG)
        form.pack(fill=tk.X, pady=(10, 6), padx=10)
        self.form_entries = {}
        for i, col in enumerate(columns):
            lbl = tk.Label(form, text=headings[i], bg=MAU_BANG, fg=MAU_CHU)
            lbl.grid(row=0, column=i, padx=8, pady=2, sticky='w')
            ent = self._create_widget(form, table_name, col, nv_options, kh_options, xm_options, i)
            self.form_entries[col] = ent
            form.columnconfigure(i, weight=1)

    def _create_widget(self, form, table_name, col, nv_options, kh_options, xm_options, i):
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
        elif table_name == 'HoaDon' and col == 'MaNV':
            ent = ttk.Combobox(form, values=nv_options, state='readonly', width=15)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
        elif table_name == 'HoaDon' and col == 'MaKH':
            ent = ttk.Combobox(form, values=kh_options, state='readonly', width=15)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
        elif table_name == 'HoaDon' and col == 'MaXe':
            ent = ttk.Combobox(form, values=xm_options, state='readonly', width=20)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='w')
            ent.bind('<<ComboboxSelected>>', lambda e: self._on_select_xm())
        elif table_name == 'HoaDon' and col == 'SoLuong':
            ent = tk.Entry(form, bg='white', fg=MAU_CHU)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
            ent.bind('<KeyRelease>', lambda e: self._calculate_total())
        elif table_name == 'HoaDon' and col == 'MaHD':
            ent = ttk.Entry(form, state='readonly')
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
        else:
            ent = tk.Entry(form, bg='white', fg=MAU_CHU)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
        return ent

    def _create_buttons(self, panel, table_name, columns):
        ttk.Separator(panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=(0, 4))
        btn_frame = tk.Frame(panel, bg=MAU_BANG)
        btn_frame.pack(fill=tk.X, pady=(4, 10), padx=10)
        btn_add = ttk.Button(btn_frame, text='Thêm', width=10, style='Primary.TButton', command=lambda: self._on_add(table_name, columns))
        btn_add.pack(side=tk.LEFT, padx=6)
        CongCuGoiY(btn_add, 'Thêm bản ghi mới')
        btn_edit = ttk.Button(btn_frame, text='Sửa', width=10, style='Primary.TButton', command=lambda: self._on_edit(table_name, columns))
        btn_edit.pack(side=tk.LEFT, padx=6)
        CongCuGoiY(btn_edit, 'Cập nhật bản ghi đã chọn')
        btn_delete = ttk.Button(btn_frame, text='Xóa', width=10, style='Primary.TButton', command=lambda: self._on_delete(table_name, columns))
        btn_delete.pack(side=tk.LEFT, padx=6)
        CongCuGoiY(btn_delete, 'Xóa bản ghi đã chọn')
        tk.Label(btn_frame, text='Tìm kiếm:', bg=MAU_BANG, fg=MAU_CHU).pack(side=tk.LEFT, padx=(20,4))
        search_ent = ttk.Entry(btn_frame)
        search_ent.pack(side=tk.LEFT, padx=4)
        btn_search = ttk.Button(btn_frame, text='Tìm', width=8, command=lambda: self._on_search(table_name, columns, search_ent.get().strip()))
        btn_search.pack(side=tk.LEFT, padx=6)
        CongCuGoiY(btn_search, 'Tìm kiếm bản ghi')
        btn_refresh = ttk.Button(btn_frame, text='Tải lại', width=8, command=lambda: self._refresh_table(table_name, columns))
        btn_refresh.pack(side=tk.RIGHT, padx=6)
        CongCuGoiY(btn_refresh, 'Tải lại dữ liệu')

    def _create_tree(self, table_name, columns, headings, display_name):
        ttk.Separator(self.content_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=(10, 4))
        tk.Label(self.content_frame, text=f'Danh sách {display_name}', font=('Arial', 16, 'bold'), bg=MAU_NEN, fg=MAU_CHINH).pack(pady=(10, 4))
        frame = tk.Frame(self.content_frame)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        for col, hd in zip(columns, headings):
            tree.heading(col, text=hd)
            tree.column(col, width=120, anchor=tk.CENTER)
        vsb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        self.current_table = table_name
        self.current_columns = columns
        self.current_tree = tree
        self._refresh_table(table_name, columns)
        tree.bind('<<TreeviewSelect>>', lambda e: self._populate_form(tree.item(tree.selection()[0], 'values') if tree.selection() else ()))
        # self.set_status(f'Xem: {table_name}')

    def _on_select_xm(self):
        selected = self.form_entries['MaXe'].get()
        if selected and ' - ' in selected:
            parts = selected.split(' - ')
            if len(parts) >= 3:
                gia_ban = parts[2]
                gia_ent = self.form_entries.get('GiaBan')
                if gia_ent:
                    gia_ent.delete(0, tk.END)
                    gia_ent.insert(0, gia_ban)
                    self._calculate_total()

    def _populate_form(self, vals):
        """Populate form with selected row values"""
        for i, col in enumerate(self.current_columns):
            if i >= len(vals):
                continue
            val = vals[i]
            ent = self.form_entries.get(col)
            if ent is None:
                continue
            if hasattr(ent, 'set'):  # Combobox or CalendarDatePicker
                ent.set(val)
            elif hasattr(ent, 'config') and ent.cget('state') == 'readonly':  # Readonly Entry
                ent.config(state='normal')
                ent.delete(0, tk.END)
                ent.insert(0, val)
                ent.config(state='readonly')
            else:  # Entry
                ent.delete(0, tk.END)
                ent.insert(0, val)

    def get_form_values(self, columns):
        vals = []
        for col in columns:
            ent = self.form_entries.get(col)
            if ent is None:
                vals.append('')
                continue
            if hasattr(ent, 'get'):
                raw = ent.get()
                if col in ['MaNV', 'MaKH', 'MaXe'] and ' - ' in raw:
                    val = raw.split(' - ')[0]
                else:
                    val = raw.strip()
            else:
                # For CalendarDatePicker
                val = ent.get().strip()
            vals.append(val)
        return vals

    def show_table(self, name):
        config = self.table_configs[name]
        self.create_table_frame(name, config['cols'], config['heads'])

    def show_nhanvien(self):
        self.show_table('NhanVien')

    def show_khachhang(self):
        self.show_table('KhachHang')

    def show_xemay(self):
        self.show_table('XeMay')

    def show_hoadon(self):
        self.show_table('HoaDon')

    def show_login(self):
        create_login_window(self)

    def show_change_password(self):
        if not self.is_admin:
            messagebox.showwarning('Không có quyền', 'Chỉ admin mới được đổi mật khẩu!')
            return
        dlg = tk.Toplevel(self.root)
        dlg.title('Đổi mật khẩu admin')
        dlg.resizable(False, False)
        # center the dialog on screen and give it a bit more height so fields are visible
        w, h = 420, 240
        sw = dlg.winfo_screenwidth()
        sh = dlg.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        dlg.geometry(f"{w}x{h}+{x}+{y}")
        dlg.transient(self.root)
        dlg.grab_set()
        try:
            dlg.configure(bg=MAU_NEN)
        except Exception:
            pass

        tk.Label(dlg, text='Mật khẩu hiện tại:', bg=MAU_NEN, fg=MAU_CHU).pack(pady=(12,4))
        cur_entry = tk.Entry(dlg, show='*', bg='white', fg=MAU_CHU)
        cur_entry.pack(padx=20)

        tk.Label(dlg, text='Mật khẩu mới:', bg=MAU_NEN, fg=MAU_CHU).pack(pady=(8,4))
        new_entry = tk.Entry(dlg, show='*', bg='white', fg=MAU_CHU)
        new_entry.pack(padx=20)

        tk.Label(dlg, text='Nhập lại mật khẩu mới:', bg=MAU_NEN, fg=MAU_CHU).pack(pady=(8,4))
        confirm_entry = tk.Entry(dlg, show='*', bg='white', fg=MAU_CHU)
        confirm_entry.pack(padx=20)

        def do_change():
            cur = cur_entry.get().strip()
            new = new_entry.get().strip()
            conf = confirm_entry.get().strip()
            if not cur or not new or not conf:
                messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ các trường')
                return
            if new != conf:
                messagebox.showerror('Lỗi', 'Mật khẩu mới không khớp')
                return
            ok = check_login('admin', cur)
            if not ok:
                messagebox.showerror('Lỗi', 'Mật khẩu hiện tại không đúng')
                return
            from modules.auth import update_admin_password
            success, msg = update_admin_password(cur, new)
            if success:
                messagebox.showinfo('Thành công', msg)
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                dlg.destroy()
            else:
                messagebox.showerror('Lỗi', msg)

        btn_frame = tk.Frame(dlg, bg=MAU_NEN)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text='Đổi mật khẩu', command=do_change, width=14, style='Primary.TButton').grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text='Hủy', command=lambda: (dlg.grab_release(), dlg.destroy()), width=8).grid(row=0, column=1, padx=6)

    def logout(self):
        """Đăng xuất người dùng hiện tại và hiển thị màn hình đăng nhập."""
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.current_user = None
            self.is_admin = False
            self.root.withdraw()
            # Hủy các widget con để tránh lỗi
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            for widget in self.khung_thanh_ben.winfo_children():
                widget.destroy()
            tao_cua_so_dang_nhap(self.root)

    # ----------------- CRUD button handlers -----------------
    def _refresh_table(self, table_name, columns):
        lam_moi_bang(self, table_name, columns)

    def _on_add(self, table_name, columns):
        khi_them(self, table_name, columns)

    def _on_edit(self, table_name, columns):
        khi_sua(self, table_name, columns)

    def _on_delete(self, table_name, columns):
        khi_xoa(self, table_name, columns)

    def _on_search(self, table_name, columns, term):
        khi_tim_kiem(self, table_name, columns, term)

    def _calculate_total(self):
        """Calculate TongThanhTien = GiaBan * SoLuong for HoaDon"""
        gia_ent = self.form_entries.get('GiaBan')
        qty_ent = self.form_entries.get('SoLuong')
        total_ent = self.form_entries.get('TongThanhTien')
        if gia_ent and qty_ent and total_ent:
            gia_str = gia_ent.get().strip()
            qty_str = qty_ent.get().strip()
            if gia_str.isdigit() and qty_str.isdigit():
                gia = int(gia_str)
                qty = int(qty_str)
                total = gia * qty
                total_ent.delete(0, tk.END)
                total_ent.insert(0, str(total))


def create_login_window(app_or_root):
    """If passed App instance, shows login and sets session; if passed root, create a temporary App after login."""
    # determine root and app
    if isinstance(app_or_root, App):
        app = app_or_root
        root = app.root
    else:
        app = None
        root = app_or_root

    login_win = tk.Toplevel(root)
    login_win.title('Đăng nhập - Quản lý Cửa hàng Xe Máy')
    login_win.resizable(False, False)
    w, h = 400, 450
    sw = login_win.winfo_screenwidth()
    sh = login_win.winfo_screenheight()
    x = (sw - w) // 2
    y = (sh - h) // 2
    login_win.geometry(f"{w}x{h}+{x}+{y}")

    # ensure it's on top
    try:
        login_win.attributes('-topmost', True)
    except Exception:
        pass
    try:
        if root.state() != 'normal':
            pass
        else:
            login_win.transient(root)
    except Exception:
        pass
    login_win.grab_set()

    login_win.configure(bg=MAU_NEN)

    # Main container
    main = tk.Frame(login_win, bg=MAU_NEN)
    main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Card container with shadow effect
    card = tk.Frame(main, bg=MAU_BANG, bd=0, relief='flat')
    card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Header section
    header = tk.Frame(card, bg=MAU_CHINH, height=60)
    header.pack(fill=tk.X)
    header.pack_propagate(False)
    title_frame = tk.Frame(header, bg=MAU_CHINH)
    title_frame.pack(padx=15, pady=15)
    tk.Label(title_frame, text='QUẢN LÝ CỬA HÀNG XE MÁY', bg=MAU_CHINH, fg='white', font=('Segoe UI', 12, 'bold')).pack(anchor='w')
    # Form section
    form = tk.Frame(card, bg=MAU_BANG)
    form.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

    # Welcome text
    tk.Label(form, text='Chào mừng bạn!', bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 18, 'bold')).pack(pady=(10,2))
    tk.Label(form, text='Vui lòng đăng nhập để tiếp tục', bg=MAU_BANG, fg='#666666', font=('Segoe UI', 11)).pack(pady=(0,15))

    # Username field
    user_frame = tk.Frame(form, bg=MAU_BANG)
    user_frame.pack(fill=tk.X, pady=(0,12))

    user_icon = tk.Label(user_frame, text='👤', bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 14))
    user_icon.pack(side=tk.LEFT, padx=(0,10))

    user_container = tk.Frame(user_frame, bg=MAU_BANG)
    user_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

    tk.Label(user_container, text='Tên đăng nhập', bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0,3))

    username_entry = tk.Entry(user_container, bg='white', fg=MAU_CHU, font=('Segoe UI', 12), relief='flat', bd=1, highlightthickness=1, highlightcolor=MAU_CHINH)
    username_entry.pack(fill=tk.X, ipady=6)

    # Password field
    pass_frame = tk.Frame(form, bg=MAU_BANG)
    pass_frame.pack(fill=tk.X, pady=(0,15))

    pass_icon = tk.Label(pass_frame, text='🔒', bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 14))
    pass_icon.pack(side=tk.LEFT, padx=(0,10))

    pass_container = tk.Frame(pass_frame, bg=MAU_BANG)
    pass_container.pack(side=tk.LEFT, fill=tk.X, expand=True)

    tk.Label(pass_container, text='Mật khẩu', bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0,3))

    password_entry = tk.Entry(pass_container, show='*', bg='white', fg=MAU_CHU, font=('Segoe UI', 12), relief='flat', bd=1, highlightthickness=1, highlightcolor=MAU_CHINH)
    password_entry.pack(fill=tk.X, ipady=6)

    # Remember me and forgot password
    options_frame = tk.Frame(form, bg=MAU_BANG)
    options_frame.pack(fill=tk.X, pady=(0,12))

    remember_var = tk.IntVar()
    remember_check = tk.Checkbutton(options_frame, text='Ghi nhớ đăng nhập', variable=remember_var, bg=MAU_BANG, fg=MAU_CHU, font=('Segoe UI', 10))
    remember_check.pack(side=tk.LEFT)

    forgot_label = tk.Label(options_frame, text='Quên mật khẩu?', fg=MAU_CHINH, bg=MAU_BANG, cursor='hand2', font=('Segoe UI', 10, 'underline'))
    forgot_label.pack(side=tk.RIGHT)

    def do_cancel():
        try:
            login_win.grab_release()
        except Exception:
            pass
        root.quit()

    def do_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror('Lỗi', 'Vui lòng nhập đầy đủ thông tin!')
            return
        if check_login(username, password):
            if app:
                app.current_user = username
                app.is_admin = (username.lower() == 'admin')
                # app.set_status('Đã đăng nhập')
                try:
                    login_win.grab_release()
                except Exception:
                    pass
                login_win.destroy()
                root.deiconify()
            else:
                root.deiconify()
                app_new = App(root)
                app_new.current_user = username
                app_new.is_admin = (username.lower() == 'admin')
                # app_new.set_status('Đã đăng nhập')
                try:
                    login_win.grab_release()
                except Exception:
                    pass
                login_win.destroy()
        else:
            messagebox.showerror('Lỗi', 'Sai tên đăng nhập hoặc mật khẩu!')

    # Login button
    login_btn = tk.Button(form, text='Đăng nhập', bg=MAU_CHINH, fg='white', font=('Segoe UI', 14, 'bold'), relief='flat', bd=0, command=do_login, padx=30, pady=10)
    login_btn.pack(pady=(8,12))

    # Hover effect for button
    login_btn.bind("<Enter>", lambda e: login_btn.config(bg=MAU_PHU))
    login_btn.bind("<Leave>", lambda e: login_btn.config(bg=MAU_CHINH))

    # Footer
    tk.Label(form, text='© 2025 - Hệ thống quản lý cửa hàng xe máy', bg=MAU_BANG, fg='#999999', font=('Segoe UI', 9)).pack(side=tk.BOTTOM, pady=(10,0))

    login_win.bind('<Return>', lambda e: do_login())
    login_win.bind('<Escape>', lambda e: do_cancel())
    username_entry.focus_set()

    try:
        login_win.update_idletasks()
        login_win.lift()
    except Exception:
        pass

    return login_win