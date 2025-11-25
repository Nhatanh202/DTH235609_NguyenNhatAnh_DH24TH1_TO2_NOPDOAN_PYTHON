import tkinter as tk
from tkinter import ttk, messagebox
from modules.auth import check_login
from modules.data import load_data
from modules.calendar import CalendarDatePicker
from modules.crud import execute_write, insert_record, update_record, delete_record, search_records, get_quantity, insert_hoa_don, generate_mahd

# Theme colors for a motorcycle shop look
PRIMARY = "#105d3b"
ACCENT = "#436007"
BG = '#f4f7fa'
PANEL = '#ffffff'
TEXT = "#000000"


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tooltip, text=self.text, background="yellow", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('Quản lý Cửa hàng Xe Máy')
        self.root.geometry('1000x650')
        self.root.state('zoomed')

        # apply theme to root
        try:
            self.root.configure(bg=BG)
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
            self.style.configure('Treeview', background=PANEL, fieldbackground=PANEL, foreground=TEXT)
            self.style.configure('Treeview.Heading', background=PRIMARY, foreground='white', font=('Segoe UI', 10, 'bold'))
            self.style.map('Treeview', background=[('selected', PRIMARY)])
            self.style.configure('evenrow', background=PANEL)
            self.style.configure('oddrow', background='#f5f5f5')
        except Exception:
            pass
        # Primary button style
        try:
            self.style.configure('Primary.TButton', background=PRIMARY, foreground='white')
            self.style.map('Primary.TButton', background=[('active', ACCENT)])
        except Exception:
            pass
        # Toolbar button style
        try:
            self.style.configure('Toolbar.TButton', background=PRIMARY, foreground='white', font=('Segoe UI', 9))
            self.style.map('Toolbar.TButton', background=[('active', ACCENT)])
        except Exception:
            pass
        # LabelFrame style for group box
        try:
            self.style.configure('TLabelFrame', background=PANEL, borderwidth=1, relief='flat')
            self.style.configure('TLabelFrame.Label', background=PANEL, foreground=PRIMARY, font=('Segoe UI', 10, 'bold'))
        except Exception:
            pass

        # session
        self.current_user = None
        self.is_admin = False

        # frames: toolbar on top and content below
        self.toolbar_frame = tk.Frame(self.root, height=56, bg=BG)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X)
        self.content_frame = tk.Frame(self.root, bg=BG)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # status bar
        self.status_var = tk.StringVar()
        status = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W, bg=PRIMARY, fg='white')
        status.pack(side=tk.BOTTOM, fill=tk.X)

        # table configs
        self.table_configs = {
            'NhanVien': {
                'cols': ('MaNV', 'HoLot', 'TenNV', 'Phai', 'NgaySinh', 'ChucVu'),
                'heads': ('Mã NV', 'Họ lót', 'Tên', 'Phái', 'Ngày sinh', 'Chức vụ')
            },
            'KhachHang': {
                'cols': ('MaKH', 'TenKH', 'SDT', 'DiaChi'),
                'heads': ('Mã KH', 'Tên KH', 'SĐT', 'Địa chỉ')
            },
            'XeMay': {
                'cols': ('MaXe', 'TenXe', 'LoaiXe', 'HangXe', 'GiaNhap', 'GiaBan', 'SoLuong'),
                'heads': ('Mã xe', 'Tên xe', 'Loại xe', 'Hãng xe', 'Giá nhập', 'Giá bán', 'Số lượng')
            },
            'HoaDon': {
                'cols': ('MaHD', 'NgayLap', 'MaNV', 'MaKH', 'MaXe', 'SoLuong', 'GiaBan', 'TongThanhTien'),
                'heads': ('Mã HD', 'Ngày lập', 'Mã NV', 'Mã KH', 'Mã xe', 'SL', 'Giá bán', 'Tổng tiền')
            }
        }

        self._build_toolbar()
        self._build_menu()
        self.show_home()

    def _build_tabs(self):
        tabs = [
            ('👤 Nhân Viên', 'NhanVien'),
            ('🛒 Khách Hàng', 'KhachHang'),
            ('🏍️ Xe Máy', 'XeMay'),
            ('📄 Hóa Đơn', 'HoaDon')
        ]
        for text, name in tabs:
            frame = tk.Frame(self.notebook, bg=BG)
            self.tab_frames[name] = frame
            self.notebook.add(frame, text=text)

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label='Đổi mật khẩu', command=self.show_change_password)
        account_menu.add_command(label='Đăng xuất', command=self.logout)
        menubar.add_cascade(label='Tài khoản', menu=account_menu)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Thoát', command=self.root.quit)

        self.root.config(menu=menubar)

    def _build_toolbar(self):
        buttons = [
            ('🏠 Trang Chủ', self.show_home, 'Về trang chủ'),
            ('👤 Nhân Viên', self.show_nhanvien, 'Quản lý nhân viên'),
            ('🛒 Khách Hàng', self.show_khachhang, 'Quản lý khách hàng'),
            ('🏍️ Xe Máy', self.show_xemay, 'Quản lý xe máy'),
            ('📄 Hóa Đơn', self.show_hoadon, 'Quản lý hóa đơn')
        ]
        for text, cmd, tip in buttons:
            btn = ttk.Button(self.toolbar_frame, text=text, command=cmd, style='Toolbar.TButton')
            btn.pack(side=tk.LEFT, padx=2)
            ToolTip(btn, tip)

    def clear_content(self, parent=None):
        if parent is None:
            parent = self.content_frame
        for w in parent.winfo_children():
            w.destroy()

    def set_status(self, text=''):
        user = self.current_user or 'Chưa đăng nhập'
        self.status_var.set(f'Người dùng: {user}    |    {text}')

    def show_home(self):
        self.clear_content()
        tk.Label(self.content_frame, text='CHÀO MỪNG ĐẾN VỚI HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY',
                 font=('Arial', 18, 'bold'), bg=BG, fg=PRIMARY).pack(pady=40)
        tk.Label(self.content_frame, text='Sử dụng menu trên để chuyển giữa các danh sách', font=('Arial', 12), bg=BG, fg=TEXT).pack()
        self.set_status('Trang chủ')

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
        panel = tk.Frame(self.content_frame, bg=PANEL, bd=1, relief='flat')
        panel.pack(fill=tk.X, padx=10, pady=(4, 10))

        self._create_form(panel, table_name, columns, headings, nv_options, kh_options, xm_options)
        self._create_buttons(panel, table_name, columns)
        self._create_tree(table_name, columns, headings, display_name)

    def _create_form(self, panel, table_name, columns, headings, nv_options, kh_options, xm_options):
        form = tk.Frame(panel, bg=PANEL)
        form.pack(fill=tk.X, pady=(10, 6), padx=10)
        self.form_entries = {}
        for i, col in enumerate(columns):
            lbl = tk.Label(form, text=headings[i], bg=PANEL, fg=TEXT)
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
            ent = tk.Entry(form, bg='white', fg=TEXT)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
            ent.bind('<KeyRelease>', lambda e: self._calculate_total())
        elif table_name == 'HoaDon' and col == 'MaHD':
            ent = ttk.Entry(form, state='readonly')
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
        else:
            ent = tk.Entry(form, bg='white', fg=TEXT)
            ent.grid(row=1, column=i, padx=8, pady=2, sticky='we')
        return ent

    def _create_buttons(self, panel, table_name, columns):
        ttk.Separator(panel, orient='horizontal').pack(fill=tk.X, padx=10, pady=(0, 4))
        btn_frame = tk.Frame(panel, bg=PANEL)
        btn_frame.pack(fill=tk.X, pady=(4, 10), padx=10)
        btn_add = ttk.Button(btn_frame, text='Thêm', width=10, style='Primary.TButton', command=lambda: self._on_add(table_name, columns))
        btn_add.pack(side=tk.LEFT, padx=6)
        ToolTip(btn_add, 'Thêm bản ghi mới')
        btn_edit = ttk.Button(btn_frame, text='Sửa', width=10, style='Primary.TButton', command=lambda: self._on_edit(table_name, columns))
        btn_edit.pack(side=tk.LEFT, padx=6)
        ToolTip(btn_edit, 'Cập nhật bản ghi đã chọn')
        btn_delete = ttk.Button(btn_frame, text='Xóa', width=10, style='Primary.TButton', command=lambda: self._on_delete(table_name, columns))
        btn_delete.pack(side=tk.LEFT, padx=6)
        ToolTip(btn_delete, 'Xóa bản ghi đã chọn')
        tk.Label(btn_frame, text='Tìm kiếm:', bg=PANEL, fg=TEXT).pack(side=tk.LEFT, padx=(20,4))
        search_ent = ttk.Entry(btn_frame)
        search_ent.pack(side=tk.LEFT, padx=4)
        btn_search = ttk.Button(btn_frame, text='Tìm', width=8, command=lambda: self._on_search(table_name, columns, search_ent.get().strip()))
        btn_search.pack(side=tk.LEFT, padx=6)
        ToolTip(btn_search, 'Tìm kiếm bản ghi')
        btn_refresh = ttk.Button(btn_frame, text='Tải lại', width=8, command=lambda: self._refresh_table(table_name, columns))
        btn_refresh.pack(side=tk.RIGHT, padx=6)
        ToolTip(btn_refresh, 'Tải lại dữ liệu')

    def _create_tree(self, table_name, columns, headings, display_name):
        ttk.Separator(self.content_frame, orient='horizontal').pack(fill=tk.X, padx=10, pady=(10, 4))
        tk.Label(self.content_frame, text=f'Danh sách {display_name}', font=('Arial', 16, 'bold'), bg=BG, fg=PRIMARY).pack(pady=(10, 4))
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
        self.set_status(f'Xem: {table_name}')

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

    def logout(self):
        self.current_user = None
        self.is_admin = False
        # show login again
        self.root.withdraw()
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
            dlg.configure(bg=BG)
        except Exception:
            pass

        tk.Label(dlg, text='Mật khẩu hiện tại:', bg=BG, fg=TEXT).pack(pady=(12,4))
        cur_entry = tk.Entry(dlg, show='*', bg='white', fg=TEXT)
        cur_entry.pack(padx=20)

        tk.Label(dlg, text='Mật khẩu mới:', bg=BG, fg=TEXT).pack(pady=(8,4))
        new_entry = tk.Entry(dlg, show='*', bg='white', fg=TEXT)
        new_entry.pack(padx=20)

        tk.Label(dlg, text='Nhập lại mật khẩu mới:', bg=BG, fg=TEXT).pack(pady=(8,4))
        confirm_entry = tk.Entry(dlg, show='*', bg='white', fg=TEXT)
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

        btn_frame = tk.Frame(dlg, bg=BG)
        btn_frame.pack(pady=12)
        ttk.Button(btn_frame, text='Đổi mật khẩu', command=do_change, width=14, style='Primary.TButton').grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text='Hủy', command=lambda: (dlg.grab_release(), dlg.destroy()), width=8).grid(row=0, column=1, padx=6)

    # ----------------- CRUD button handlers -----------------
    def _refresh_table(self, table_name, columns):
        self.set_status('Đang tải dữ liệu...')
        # clear tree
        tree = getattr(self, 'current_tree', None)
        if tree is None:
            return
        for r in tree.get_children():
            tree.delete(r)
        data = load_data(table_name)
        for idx, row in enumerate(data):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert('', tk.END, values=row, tags=(tag,))
        self.set_status('Sẵn sàng')

    def _on_add(self, table_name, columns):
        self.set_status('Đang thêm bản ghi...')
        vals = self.get_form_values(columns)
        if table_name == 'HoaDon':
            vals[0] = generate_mahd()  # Luôn generate MaHD mới
            # Set back to form
            mahd_ent = self.form_entries.get('MaHD')
            if mahd_ent:
                mahd_ent.config(state='normal')
                mahd_ent.delete(0, tk.END)
                mahd_ent.insert(0, vals[0])
                mahd_ent.config(state='readonly')
        elif not vals[0]:
            # allow user to enter primary key; if empty warn
            messagebox.showwarning('Lỗi', 'Mã (khóa chính) không được để trống')
            self.set_status('Sẵn sàng')
            return
        # Validate data
        if not self._validate_data(table_name, columns, vals):
            self.set_status('Sẵn sàng')
            return
        data = dict(zip(columns, vals))
        if table_name == 'HoaDon':
            ok = insert_hoa_don(data)
            if ok:
                self._refresh_table(table_name, columns)
                # Also refresh XeMay table if visible
                if hasattr(self, 'current_table') and self.current_table == 'XeMay':
                    xemay_columns = self.table_configs['XeMay']['cols']
                    self._refresh_table('XeMay', xemay_columns)
            else:
                messagebox.showerror('Lỗi', 'Không thể thêm hóa đơn. Lỗi cơ sở dữ liệu.')
        else:
            ok = insert_record(table_name, data)
            if ok:
                messagebox.showinfo('Thành công', f'Đã thêm {table_name} thành công!')
                self._refresh_table(table_name, columns)
            else:
                messagebox.showerror('Lỗi', f'Không thể thêm {table_name}. Lỗi cơ sở dữ liệu.')
        self.set_status('Sẵn sàng')

    def _on_edit(self, table_name, columns):
        self.set_status('Đang cập nhật...')
        vals = self.get_form_values(columns)
        if not vals[0]:
            messagebox.showwarning('Lỗi', 'Chọn hoặc nhập Mã để sửa')
            self.set_status('Sẵn sàng')
            return
        # Validate data (skip primary key)
        if not self._validate_data(table_name, columns[1:], vals[1:]):
            self.set_status('Sẵn sàng')
            return
        data = dict(zip(columns[1:], vals[1:]))
        where_clause = f"{columns[0]} = ?"
        where_params = (vals[0],)
        ok = update_record(table_name, data, where_clause, where_params)
        if ok:
            messagebox.showinfo('Thành công', f'Đã cập nhật {table_name} thành công!')
            self._refresh_table(table_name, columns)
        else:
            messagebox.showerror('Lỗi', f'Không thể cập nhật {table_name}. Lỗi cơ sở dữ liệu.')
        self.set_status('Sẵn sàng')

    def _on_delete(self, table_name, columns):
        self.set_status('Đang xóa...')
        pk = columns[0]
        pkval = self.form_entries[pk].get().strip()
        if not pkval:
            messagebox.showwarning('Lỗi', 'Chọn hoặc nhập Mã để xóa')
            self.set_status('Sẵn sàng')
            return
        if not messagebox.askyesno('Xác nhận', f'Bạn có chắc muốn xóa {pkval}?'):
            self.set_status('Sẵn sàng')
            return
        where_clause = f"{pk} = ?"
        where_params = (pkval,)
        ok = delete_record(table_name, where_clause, where_params)
        if ok:
            messagebox.showinfo('Thành công', f'Đã xóa {table_name} thành công!')
            self._refresh_table(table_name, columns)
        else:
            messagebox.showerror('Lỗi', f'Không thể xóa {table_name}. Lỗi cơ sở dữ liệu.')
        self.set_status('Sẵn sàng')

    def _on_search(self, table_name, columns, term):
        tree = getattr(self, 'current_tree', None)
        if tree is None:
            return
        for r in tree.get_children():
            tree.delete(r)
        if not term:
            self._refresh_table(table_name, columns)
            return
        rows = search_records(table_name, columns, term)
        for row in rows:
            tree.insert('', tk.END, values=row)

    def _validate_data(self, table_name, columns, vals):
        """Validate input data before insert/update"""
        for i, col in enumerate(columns):
            val = vals[i]
            if table_name == 'HoaDon' and col == 'MaHD':
                continue  # MaHD is auto-generated
            if not val:
                messagebox.showwarning('Lỗi', f'{col} không được để trống')
                return False
            if col in ['GiaNhap', 'GiaBan']:
                if not val.isdigit() or int(val) <= 0:
                    messagebox.showwarning('Lỗi', f'{col} phải là số dương')
                    return False
            elif col == 'SoLuong':
                if not val.isdigit() or int(val) < 0:
                    messagebox.showwarning('Lỗi', f'{col} phải là số không âm')
                    return False
            elif col in ['SDT']:
                if val and not val.isdigit():
                    messagebox.showwarning('Lỗi', f'{col} phải là số')
                    return False
            # Check foreign keys for HoaDon
            if table_name == 'HoaDon':
                if col == 'MaNV':
                    if not self._check_exists('NhanVien', 'MaNV', val):
                        messagebox.showwarning('Lỗi', f'Mã nhân viên {val} không tồn tại')
                        return False
                elif col == 'MaKH':
                    if not self._check_exists('KhachHang', 'MaKH', val):
                        messagebox.showwarning('Lỗi', f'Mã khách hàng {val} không tồn tại')
                        return False
                elif col == 'MaXe':
                    if not self._check_exists('XeMay', 'MaXe', val):
                        messagebox.showwarning('Lỗi', f'Mã xe {val} không tồn tại')
                        return False
            # Add more validations as needed
        return True

    def _check_exists(self, table, column, value):
        """Check if value exists in table.column"""
        from modules.data import load_data
        data = load_data(table)
        for row in data:
            if str(row[0]) == str(value):  # Assuming first column is key
                return True
        return False

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
    login_win.title('Đăng nhập')
    login_win.resizable(False, False)
    w, h = 360, 220
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
            # don't set transient when root is withdrawn
            pass
        else:
            login_win.transient(root)
    except Exception:
        pass
    login_win.grab_set()

    tk.Label(login_win, text='Tên đăng nhập:').pack(pady=(15,5))
    username_entry = tk.Entry(login_win)
    username_entry.pack(padx=20)

    tk.Label(login_win, text='Mật khẩu:').pack(pady=(10,5))
    password_entry = tk.Entry(login_win, show='*')
    password_entry.pack(padx=20)

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
                app.set_status('Đã đăng nhập')
                try:
                    login_win.grab_release()
                except Exception:
                    pass
                login_win.destroy()
                root.deiconify()
            else:
                # create app now
                root.deiconify()
                app_new = App(root)
                app_new.current_user = username
                app_new.is_admin = (username.lower() == 'admin')
                app_new.set_status('Đã đăng nhập')
                try:
                    login_win.grab_release()
                except Exception:
                    pass
                login_win.destroy()
        else:
            messagebox.showerror('Lỗi', 'Sai tên đăng nhập hoặc mật khẩu!')

    btn_frame = tk.Frame(login_win)
    btn_frame.pack(pady=15)
    ttk.Button(btn_frame, text='Đăng nhập', width=12, command=do_login, style='Primary.TButton').grid(row=0, column=0, padx=6)
    ttk.Button(btn_frame, text='Thoát', width=8, command=do_cancel).grid(row=0, column=1, padx=6)

    login_win.bind('<Return>', lambda e: do_login())
    login_win.bind('<Escape>', lambda e: do_cancel())
    username_entry.focus_set()

    try:
        login_win.update_idletasks()
        login_win.lift()
    except Exception:
        pass

    return login_win