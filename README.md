# HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY
Motorbike Store Management System

<div align="center">
<img src="Image/logo.png" alt="Logo Dự Án" width="180" style="border-radius: 50%; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);"/>
<br><br>
<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</a>
<a href="https://docs.python.org/3/library/tkinter.html">
    <img src="https://img.shields.io/badge/GUI-Tkinter-green?style=for-the-badge&logo=gui&logoColor=white" alt="Tkinter">
</a>
<a href="https://www.microsoft.com/en-us/sql-server/">
    <img src="https://img.shields.io/badge/Database-SQL%20Server-red?style=for-the-badge&logo=microsoft-sql-server&logoColor=white" alt="SQL Server">
</a>
</div>

<br>

📖 GIỚI THIỆU TỔNG QUAN
---
Đồ án Môn học: **Chuyên đề Python (COS525)**

Dự án là giải pháp phần mềm toàn diện giúp các đại lý xe máy số hóa quy trình quản lý. Từ nhập kho, quản lý nhân sự, chăm sóc khách hàng đến xuất hóa đơn bán hàng, mọi thao tác đều được thực hiện nhanh chóng trên giao diện trực quan.

**Mục tiêu chính:** Tối ưu hóa hiệu quả kinh doanh, giảm thiểu sai sót thủ công và cung cấp cái nhìn tổng quan về tình hình hoạt động của cửa hàng.

🌟 TÍNH NĂNG NỔI BẬT
---
Hệ thống được chia thành các module chức năng chuyên biệt:

| Module             | Icon | Mô tả chi tiết                                                               |
| :----------------- | :--- | :--------------------------------------------------------------------------- |
| Quản lý Xe Máy     | 🏍️   | Theo dõi thông số kỹ thuật, giá bán, màu sắc và số khung của từng mẫu xe.    |
| Quản lý Nhân viên  | 👥   | Quản lý hồ sơ nhân viên, chức vụ và thông tin cá nhân.                       |
| Quản lý Khách hàng | 🤝   | Lưu trữ thông tin khách hàng (Tên, SĐT, Địa chỉ) và lịch sử giao dịch.       |
| Quản lý Hóa đơn    | 🧾   | Lập hóa đơn bán hàng, xem chi tiết sản phẩm và tính tổng tiền tự động.       |
| Quản lý Tài khoản  | 🔐   | Quản lý tài khoản đăng nhập, phân quyền và bảo mật thông tin.                |

🛠️ CÔNG NGHỆ & KỸ THUẬT
---
Dự án áp dụng các công nghệ và kỹ thuật lập trình hiện đại:

* **Ngôn ngữ:** Python 3.x (Hướng đối tượng - OOP).
* **Giao diện (GUI):** Tkinter với `ttk` styling để tạo giao diện hiện đại, responsive.
* **Cơ sở dữ liệu:** Microsoft SQL Server (Lưu trữ bền vững, quan hệ chặt chẽ).
* **Kết nối:** Thư viện `pyodbc` (Chuẩn kết nối ODBC hiệu suất cao).
* **Tiện ích:** `Pillow` (Xử lý ảnh), `tkcalendar` (Lịch chọn ngày thông minh).

📂 CẤU TRÚC DỰ ÁN
---
Mã nguồn được tổ chức rõ ràng theo thư mục chức năng:

```text
DTH235609_NguyenNhatAnh_DH24TH1_TO2_NOPDOAN_PYTHON/
│
├── 📂 GUI/                     # MÃ NGUỒN GIAO DIỆN & LOGIC
│   ├── Login.py                # Màn hình Đăng nhập hệ thống
│   ├── main.py                 # Màn hình Dashboard chính
│   ├── quanly_hoadon.py        # Module quản lý hóa đơn bán hàng
│   ├── quanly_khachhang.py     # Module quản lý thông tin khách hàng
│   ├── quanly_nhanvien.py      # Module quản lý hồ sơ nhân viên
│   ├── quanly_taikhoan.py      # Module quản lý tài khoản người dùng
│   ├── quanly_xemay.py         # Module quản lý kho xe máy
│   ├── thongtin_taikhoan.py    # Xem và chỉnh sửa thông tin cá nhân
│   └── utils.py                # Các hàm tiện ích chung & Kết nối CSDL
│
├── 📂 Image/                   # TÀI NGUYÊN HÌNH ẢNH
│   ├── logo.png                # Logo thương hiệu
│   └── User.png                # Icon đại diện người dùng
│
├── 🗄️ QLCHXM.sql               # Script khởi tạo CSDL SQL Server
└── 📄 README.md                # Tài liệu hướng dẫn sử dụng
