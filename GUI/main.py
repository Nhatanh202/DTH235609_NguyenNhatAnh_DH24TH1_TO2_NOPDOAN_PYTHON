from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import utils
import quanly_xemay
import quanly_nhanvien 
import quanly_khachhang
import quanly_hoadon
import quanly_taikhoan
import thongtin_taikhoan

class MainApp:
    def __init__(self, root, role, fullname):
        self.root = root
        self.role = role
        self.fullname = fullname
        self.root.title("Hệ Thống Quản Lý Cửa Hàng Xe Máy")
        self.root.state('zoomed') # Mở toàn màn hình
        
        utils.setup_theme(root)

        # --- LAYOUT CHÍNH: CHIA 2 CỘT ---
        # Cột 1: Menu bên trái (Sidebar)
        self.sidebar = Frame(root, bg=utils.BTN_PRIMARY, width=250)
        self.sidebar.pack(side=LEFT, fill=Y)
        self.sidebar.pack_propagate(False) # Cố định chiều rộng

        # Cột 2: Nội dung bên phải
        self.content_area = Frame(root, bg="white")
        self.content_area.pack(side=RIGHT, fill=BOTH, expand=True)

        # --- NỘI DUNG SIDEBAR ---
        # Info user
        Label(self.sidebar, text=f"XIN CHÀO,\n{fullname}", font=("Roboto", 12, "bold"), 
              bg=utils.BTN_PRIMARY, fg="white", justify=CENTER).pack(pady=(20, 5)) # Giảm khoảng cách dưới
        img = Image.open("Image/User.png").resize((80, 80))
        img_tk = ImageTk.PhotoImage(img)
        label_img = Label(self.sidebar, image=img_tk, bg=utils.BTN_PRIMARY)
        label_img.image = img_tk
        label_img.pack(pady=0) # Bỏ khoảng đệm của ảnh
        
        Label(self.sidebar, text=f"Vai trò: {role}", font=("Roboto", 10, "italic"), 
              bg=utils.BTN_PRIMARY, fg="white").pack(pady=(5, 20)) # Giảm khoảng cách trên

        # MENU BUTTONS
        self.create_nav_btn("Trang Chủ", self.show_home)

        self.create_nav_btn("Quản Lý Xe Máy", self.show_xemay)
        
        if self.role in ['Admin', 'QuanLy']:
            self.create_nav_btn("Quản Lý Nhân Viên", self.show_nhanvien)
        
        self.create_nav_btn("Quản Lý Khách Hàng", self.show_khachhang)

        self.create_nav_btn("Hóa Đơn & Bán Hàng", self.show_hoadon)

        if role == 'Admin':
            self.create_nav_btn("Quản Lý Tài Khoản", self.show_taikhoan)

        self.create_nav_btn("Thông Tin Tài Khoản", self.show_thongtin_taikhoan)
        
        # Nút Đăng xuất ở dưới cùng
        Button(self.sidebar, text="Đăng Xuất", command=self.logout, 
               bg="#c0392b", fg="white", relief="flat").pack(side=BOTTOM, fill=X, pady=10, padx=10)

        # Mặc định hiện trang chủ
        self.show_home()

    def logout(self):
        self.root.destroy()
        # Import tại đây để tránh lỗi import vòng
        import Login 
        tk = Tk()
        Login.LoginApp(tk)
        tk.mainloop()

    def create_nav_btn(self, text, command):
        btn = Button(self.sidebar, text=text, command=command,
                     bg=utils.BTN_PRIMARY, fg="white",
                     font=("Roboto", 11), anchor="w", padx=20, pady=10,
                     activebackground=utils.NAV_HOVER, activeforeground="white",
                     relief="flat", bd=0)
        btn.pack(fill=X)

    def clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    # --- CÁC HÀM CHUYỂN TRANG ---
    def show_home(self):
        self.clear_content()
        
        # --- Center Frame ---
        center_frame = Frame(self.content_area, bg="white")
        center_frame.pack(expand=True)

        # Logo
        img = Image.open("Image/logo.png").resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        label_img = Label(center_frame, image=img_tk, bg="white")
        label_img.image = img_tk  # Giữ tham chiếu để ảnh không bị
        label_img.pack(pady=(0, 10)) # Khoảng cách dưới logo

        # Text
        Label(center_frame, text="QUẢN LÝ CỬA HÀNG XE MÁY", 
              font=("Roboto", 24, "bold"), fg=utils.BTN_PRIMARY, bg="white").pack()

    def show_xemay(self):
        self.clear_content()
        quanly_xemay.create_ui(self.content_area)

    def show_nhanvien(self):
        self.clear_content()
        quanly_nhanvien.create_ui(self.content_area)
        
    def show_khachhang(self):
        self.clear_content()
        quanly_khachhang.create_ui(self.content_area)

    def show_hoadon(self):
        self.clear_content()
        quanly_hoadon.create_ui(self.content_area)

    def show_taikhoan(self):
        self.clear_content()
        quanly_taikhoan.create_ui(self.content_area)
    
    def show_thongtin_taikhoan(self):
        self.clear_content()
        thongtin_taikhoan.create_ui(self.content_area)

def main_screen(role, fullname):
    root = Tk()
    app = MainApp(root, role, fullname)
    root.mainloop()