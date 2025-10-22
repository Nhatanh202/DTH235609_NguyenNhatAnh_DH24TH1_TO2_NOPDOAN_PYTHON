import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
# Import hàm kết nối từ module database
# Tạm thời chưa import CRUD vì Huy đang code
# from modules.crud import load_data, them_xe, ... 

# ====== HÀM CĂN GIỮA CỬA SỔ (Lấy từ mẫu) ======
def center_window(win, w=850, h=550): # Đặt kích thước lớn hơn để chứa nhiều cột xe máy
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("QUẢN LÝ CỬA HÀNG XE MÁY") # Thay thế tiêu đề Quản lý Nhân viên
center_window(root)
root.resizable(False, False)

# ====== TIÊU ĐỀ ======
lbl_title = tk.Label(root, text="QUẢN LÝ CỬA HÀNG XE MÁY", font=("Roboto", 18, "bold"))
lbl_title.pack(pady=10)
# ... (Phần code định nghĩa Form, Treeview, Buttons)

# ====== CHẠY VÒNG LẶP CHÍNH (BẮT BUỘC) ======
if __name__ == "__main__":
    root.mainloop()