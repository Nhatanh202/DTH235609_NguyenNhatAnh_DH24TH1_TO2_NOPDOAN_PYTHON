import tkinter as tk
from tkinter import ttk, messagebox



def center_window(win, w=900, h=600):
    # Hàm căn giữa cửa sổ
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

root = tk.Tk()
root.title("QUẢN LÝ CỬA HÀNG XE MÁY")
center_window(root)
root.resizable(False, False)

tk.Label(root, text="HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY", font=("Arial", 20, "bold"), fg="red").pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(pady=5, padx=10, expand=True, fill="both")

# Khai báo các Frame (Tab)
frame_xemay = ttk.Frame(notebook)
frame_nhanvien = ttk.Frame(notebook)
frame_khachhang = ttk.Frame(notebook)
frame_hoadon = ttk.Frame(notebook)

# Thêm các Frame vào Notebook
notebook.add(frame_xemay, text='Quản lý Xe Máy')
notebook.add(frame_nhanvien, text='Quản lý Nhân Viên')
notebook.add(frame_khachhang, text='Quản lý Khách Hàng')
notebook.add(frame_hoadon, text='Quản lý Hóa Đơn')


root.mainloop()