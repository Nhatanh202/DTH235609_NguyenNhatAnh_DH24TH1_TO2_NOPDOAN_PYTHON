import tkinter as tk
from tkinter import messagebox
from modules.auth import check_login
from modules.constants import MAU_CHINH, MAU_PHU, MAU_NEN, MAU_BANG, MAU_CHU


def tao_cua_so_dang_nhap(app_or_root):
    """Nếu truyền instance App, hiển thị login và thiết lập session; nếu truyền root, tạo App tạm thời sau khi login."""
    # determine root and app
    if hasattr(app_or_root, 'root'):  # Check if it's an App instance
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
                # Import here to avoid circular import
                from modules.gui import App
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
    btn_frame = tk.Frame(form, bg=MAU_BANG)
    btn_frame.pack(pady=(8,12))
    login_btn = tk.Button(btn_frame, text='Đăng nhập', bg=MAU_CHINH, fg='white', font=('Segoe UI', 14, 'bold'), relief='flat', bd=0, command=do_login, padx=20, pady=10)
    login_btn.pack(side=tk.LEFT, padx=10)
    cancel_btn = tk.Button(btn_frame, text='Hủy', bg='#666666', fg='white', font=('Segoe UI', 14, 'bold'), relief='flat', bd=0, command=do_cancel, padx=20, pady=10)
    cancel_btn.pack(side=tk.LEFT, padx=10)

    # Hover effect for buttons
    login_btn.bind("<Enter>", lambda e: login_btn.config(bg=MAU_PHU))
    login_btn.bind("<Leave>", lambda e: login_btn.config(bg=MAU_CHINH))
    cancel_btn.bind("<Enter>", lambda e: cancel_btn.config(bg='#888888'))
    cancel_btn.bind("<Leave>", lambda e: cancel_btn.config(bg='#666666'))

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