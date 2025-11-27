<div align="center">

# HỆ THỐNG QUẢN LÝ CỬA HÀNG XE MÁY
**Motorbike Store Management System**

<img src="Image/logo.png" alt="Logo Dự Án" width="160" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);"/>

<br><br>

<a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
</a>
<a href="https://docs.python.org/3/library/tkinter.html">
    <img src="https://img.shields.io/badge/GUI-Tkinter-2C5F2D?style=for-the-badge&logo=gui&logoColor=white" alt="Tkinter">
</a>
<a href="https://www.microsoft.com/en-us/sql-server/">
    <img src="https://img.shields.io/badge/DB-SQL%20Server-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white" alt="SQL Server">
</a>

</div>

---

## 📖 GIỚI THIỆU TỔNG QUAN

**Đồ án Môn học:** Chuyên đề Python (COS525)  
**Trường:** Đại học An Giang

Dự án là giải pháp phần mềm toàn diện giúp các đại lý xe máy số hóa quy trình quản lý. Từ nhập kho, quản lý nhân sự, chăm sóc khách hàng đến xuất hóa đơn bán hàng, mọi thao tác đều được thực hiện nhanh chóng trên giao diện trực quan.

> 🎯 **Mục tiêu:** Tối ưu hóa hiệu quả kinh doanh, giảm thiểu sai sót thủ công và cung cấp cái nhìn tổng quan về tình hình hoạt động của cửa hàng.

---

## 🌟 TÍNH NĂNG NỔI BẬT

Hệ thống được chia thành các module chức năng chuyên biệt:

| Module | Icon | Mô tả chi tiết |
| :--- | :---: | :--- |
| **Quản lý Xe Máy** | 🏍️ | Theo dõi thông số kỹ thuật, giá bán, màu sắc, số khung và tình trạng tồn kho. |
| **Quản lý Nhân viên** | 👥 | Quản lý hồ sơ nhân viên, chức vụ, thông tin cá nhân và lương thưởng. |
| **Quản lý Khách hàng** | 🤝 | Lưu trữ data khách hàng (Tên, SĐT, Địa chỉ) phục vụ CSKH và bảo hành. |
| **Quản lý Hóa đơn** | 🧾 | Lập hóa đơn bán hàng (Master-Detail), tự động tính tổng tiền và lưu lịch sử. |
| **Hệ thống Bảo mật** | 🔐 | Đăng nhập an toàn, phân quyền Admin/Nhân viên, quản lý tài khoản. |

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

Dự án áp dụng các công nghệ và kỹ thuật lập trình hiện đại:

* **Ngôn ngữ:** Python 3.x (Lập trình hướng đối tượng - OOP).
* **Giao diện (GUI):** Thư viện `Tkinter` kết hợp `ttk` để tạo giao diện hiện đại, responsive.
* **Cơ sở dữ liệu:** Microsoft SQL Server.
* **Kết nối:** Thư viện `pyodbc` (Chuẩn kết nối ODBC hiệu suất cao).
* **Tiện ích mở rộng:** * `Pillow` (Xử lý và hiển thị hình ảnh).
    * `tkcalendar` (Lịch chọn ngày tháng thông minh).

---

## 📂 CẤU TRÚC DỰ ÁN

Mã nguồn được tổ chức theo cấu trúc module hóa, tách biệt giao diện và logic:

```text
DTH2356.../
│
├── 📂 GUI/                     # MÃ NGUỒN GIAO DIỆN & LOGIC
│   ├── Login.py                # Màn hình Đăng nhập
│   ├── main.py                 # Màn hình Dashboard chính
│   ├── quanly_hoadon.py        # Module Hóa đơn
│   ├── quanly_khachhang.py     # Module Khách hàng
│   ├── quanly_nhanvien.py      # Module Nhân viên
│   ├── quanly_taikhoan.py      # Quản lý tài khoản Admin
│   ├── quanly_xemay.py         # Module Kho xe
│   ├── thongtin_taikhoan.py    # Xem thông tin cá nhân
│   └── utils.py                # Các hàm tiện ích & Kết nối DB
│
├── 📂 Image/                   # TÀI NGUYÊN HÌNH ẢNH
│   ├── logo.png                # Logo hiển thị trên App
│   └── User.png                # Avatar mặc định
│
├── 🗄️ QLCHXM.sql               # Script khởi tạo Database SQL
└── 📄 README.md                # Tài liệu dự án

```
## 🔑 TÀI KHOẢN MẶC ĐỊNH
Sử dụng tài khoản quản trị viên để đăng nhập lần đầu:

| Vai trò | Tên đăng nhập | Mật khẩu |
| :--- | :---: | :--- |
| **Admin** | admin | 123 |

## 👨‍💻ĐỘI NGŨ PHÁT TRIỂN
| Thành viên | MSSV | Nhiệm vụ |
| :--- | :---: | :--- |
| **Nguyễn Nhất Anh** | DTH235609 |  CSDL, code, thiết kế giao diện |
| **Phạm Hữu Huy** | DTH235665 |  CSDL, code, thiết kế giao diện |

<div align = "center" , style = "border-radius: 10px">
<b>Giảng viên hướng dẫn: ThS. Nguyễn Ngọc Minh</b>

<div align="center", width="160" style="border-radius: 10px; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2)?


<i>Đồ án môn học - Khoa Công Nghệ Thông Tin - Đại học An Giang © 2025</i> </div>
