import tkinter as tk
from tkinter import ttk, messagebox
# from tkcalendar import DateEntry # Thêm nếu cần

# --- Khai báo các hàm xử lý Menu (Command Handlers) ---
# Tạm thời, các hàm này chỉ in ra thông báo, sau này bạn sẽ thay thế bằng code gọi các Form quản lý.
def show_form_hanghoa():
    messagebox.showinfo("Chức năng", "Mở Form Quản lý Xe Máy (Hàng hóa)")
    # Ở đây, bạn sẽ chuyển đổi/hiển thị Frame chứa nội dung Quản lý Xe Máy

def show_form_nhanvien():
    messagebox.showinfo("Chức năng", "Mở Form Quản lý Nhân Viên")

def show_form_khachhang():
    messagebox.showinfo("Chức năng", "Mở Form Quản lý Khách Hàng")

# ... (Thêm các hàm cho các mục menu khác: Báo cáo, Trợ giúp, v.v.)

# ====== CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("Chương trình Quản lý Cửa Hàng Xe Máy")
# (Thêm center_window() và resizable(False, False) nếu cần)

# -----------------------------------------------------------
# --- 1. TẠO THANH MENU CHÍNH (MENU BAR) ---
# -----------------------------------------------------------
menubar = tk.Menu(root)
root.config(menu=menubar) # Gán Menu Bar vào cửa sổ chính

# -----------------------------------------------------------
# --- 2. TẠO CÁC MENU CẤP 1 (Tập tin, Danh mục, Hóa đơn...) ---
# -----------------------------------------------------------

# === 2a. Menu 'Tập tin' ===
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Tập tin", menu=file_menu)
file_menu.add_command(label="Đóng", command=root.quit) # Ví dụ: Thoát ứng dụng

# === 2b. Menu 'Danh mục' (Chứa các Form Quản lý CRUD) ===
danhmuc_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Danh mục", menu=danhmuc_menu)

# Menu con cho Danh mục (Mô phỏng 4 Form của bạn)
# Chú ý: Xe Máy tương đương với Hàng hoá trong mẫu
danhmuc_menu.add_command(label="Xe Máy (Hàng hoá)", command=show_form_hanghoa) 
danhmuc_menu.add_command(label="Nhân viên", command=show_form_nhanvien)
danhmuc_menu.add_command(label="Khách hàng", command=show_form_khachhang)
danhmuc_menu.add_separator() # Đường kẻ phân cách
danhmuc_menu.add_command(label="Chất liệu/Loại xe", command=lambda: print("Mở Form Chất liệu"))


# === 2c. Menu 'Hoá đơn' ===
hoadon_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Hóa đơn", menu=hoadon_menu)
hoadon_menu.add_command(label="Lập hóa đơn", command=lambda: print("Lập HĐ"))
hoadon_menu.add_command(label="Xem danh sách HĐ", command=lambda: print("Xem HĐ"))

# -----------------------------------------------------------
# --- 3. KHU VỰC CHÍNH (FRAME CHỨA NỘI DUNG CÁC FORM) ---
# -----------------------------------------------------------
# Do bạn không dùng hệ thống Tab Notebook nữa, bạn cần một Frame chính để hiển thị nội dung.

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Ví dụ: Hiển thị nội dung chào mừng ban đầu
tk.Label(main_frame, text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG XE MÁY", 
         font=("Arial", 20), fg="#336699").pack(pady=50)


# ====== CHẠY VÒNG LẶP CHÍNH ======
if __name__ == "__main__":
    root.mainloop()