from tkinter import *
from tkinter import messagebox
import hashlib
import utils
import main 
from PIL import Image, ImageTk

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng Nhập")
        
        # --- Căn giữa cửa sổ ---
        window_width = 400
        window_height = 450 # Tăng chiều cao để chứa logo
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.root.resizable(False, False) # Không cho thay đổi kích thước

        # --- Thêm Logo ---
        img = Image.open("Image/logo.png").resize((100, 100))
        img_tk = ImageTk.PhotoImage(img)
        label_img = Label(root, image=img_tk)
        label_img.image = img_tk
        label_img.pack(pady=(20, 0))
        
        Label(root, text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY", font=("Roboto", 13, "bold"), fg= utils.BTN_PRIMARY).pack(pady=(10, 20))
        
        frame = Frame(root)
        frame.pack(pady=10)
        
        Label(frame, text="Tài khoản:").grid(row=0, column=0, pady=10, padx=5)
        self.txt_user = Entry(frame, width=30, font=("Roboto", 10, "bold"))
        self.txt_user.grid(row=0, column=1)
        
        Label(frame, text="Mật khẩu:").grid(row=1, column=0, pady=10, padx=5)
        self.txt_pass = Entry(frame, width=30, show="*", font=("Roboto", 10, "bold"))
        self.txt_pass.grid(row=1, column=1)
        
        # Frame chứa các nút
        button_frame = Frame(root)
        button_frame.pack(pady=20)

        Button(button_frame, text="Đăng Nhập", command=self.login, bg=utils.BTN_PRIMARY, fg="white", width=15, font=("Roboto", 11, "bold"), relief="flat", pady=5).pack(side=LEFT, padx=10)
        Button(button_frame, text="Thoát", command=self.root.destroy, bg="#c0392b", fg="white", width=15, font=("Roboto", 11, "bold"), relief="flat", pady=5).pack(side=LEFT, padx=10)

    def login(self):
        user = self.txt_user.get()
        pwd = hashlib.sha256(self.txt_pass.get().encode()).hexdigest()
        
        conn = utils.get_connection()
        if conn:
            cursor = conn.cursor()
            # Lấy thông tin VaiTro, HoTen, MaNhanVien
            sql = "SELECT TK.VaiTro, NV.HoVaTen, NV.MaNhanVien FROM TaiKhoan TK JOIN NhanVien NV ON TK.MaNhanVien=NV.MaNhanVien WHERE TK.TenDangNhap=? AND TK.MatKhau=?"
            cursor.execute(sql, (user, pwd))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                # --- LƯU VÀO BIẾN TOÀN CỤC (QUAN TRỌNG) ---
                utils.current_user['role'] = row[0]  # Vai trò
                utils.current_user['name'] = row[1]  # Họ tên
                utils.current_user['id'] = row[2]    # Mã nhân viên
                
                self.root.destroy()
                main.main_screen(row[0], row[1])
            else:
                messagebox.showerror("Lỗi", "Sai tài khoản hoặc mật khẩu!")

if __name__ == "__main__":
    tk = Tk()
    LoginApp(tk)
    tk.mainloop()