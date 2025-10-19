# BÁO CÁO ĐỒ ÁN  
## CHUYÊN ĐỀ PYTHON (COS525)

- **Đề tài:** XÂY DỰNG ỨNG DỤNG QUẢN LÝ XE MÁY
- **Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh  
- **Trường:** Đại học An Giang – Khoa Công nghệ Thông tin  

---

## THÀNH VIÊN

| STT | Họ và tên | MSSV | Lớp | Nhóm | Tổ |
|-----|------------|------|------|------|----|
| 1 | Nguyễn Nhất Anh | DH235609 | DH24TH1 | Nhóm 1 | Tổ 2 |
| 2 | Phạm Hữu Huy | DH235665 | DH24TH1 | Nhóm 1 | Tổ 2 |

---

Đề tài **“Quản lý xe máy”** nhằm xây dựng một ứng dụng đơn giản giúp người dùng thực hiện các thao tác **thêm, sửa, xóa, lưu và tìm kiếm thông tin xe máy** thông qua giao diện trực quan được phát triển bằng **Python – Tkinter** và lưu trữ dữ liệu bằng **MySQL**.

---

## 1. TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT

### a) Kiến thức áp dụng
- Lập trình hướng đối tượng trong Python  
- Xây dựng giao diện đồ họa người dùng với **Tkinter**  
- Kết nối và xử lý dữ liệu với **MySQL**  
- Sử dụng `mysql-connector-python` để truy vấn CSDL  
- Thao tác CRUD (Create, Read, Update, Delete)  
- Áp dụng thư viện `tkcalendar` cho chọn ngày  

### b) Công nghệ sử dụng

| Thành phần | Công nghệ |
|-------------|------------|
| Ngôn ngữ lập trình | **Python** |
| Giao diện người dùng | **Tkinter** |
| Cơ sở dữ liệu | **MySQL** |
| Thư viện hỗ trợ | `mysql-connector-python`, `tkcalendar`, `pillow` |
| IDE khuyến nghị | Visual Studio Code / PyCharm |

---

## 3. CẤU TRÚC THƯ MỤC DỰ ÁN  
QuanLyXeMay/
├── main.py                  # File chính chạy ứng dụng
├── database/
│   ├── connect.py           # Kết nối MySQL
│   └── setup.sql            # Câu lệnh tạo cơ sở dữ liệu & bảng
├── modules/
│   ├── crud.py              # Các hàm thêm, sửa, xóa, tìm kiếm
│   └── utils.py             # Hàm tiện ích khác (validate, format,...)
├── assets/
│   ├── icons/               # Icon, hình ảnh giao diện
│   └── logo.png
├── README.md                # Mô tả dự án
└── requirements.txt         # Danh sách thư viện cần

---

## 4. KIẾN THỨC VẬN DỤNG  
- Lập trình Python kết hợp GUI và cơ sở dữ liệu.
- Kỹ thuật CRUD (Thêm – Sửa – Xóa – Xem).
- Tạo giao diện bằng Tkinter và Treeview.
- Kết nối và xử lý dữ liệu với MySQL.
- Kỹ năng làm việc nhóm và quản lý dự án phần mềm nhỏ.

---

## 5. TÀI LIỆU THAM KHẢO

- Tài liệu hướng dẫn đồ án môn Python – ThS. Nguyễn Ngọc Minh  
- [Python Official Documentation](https://docs.python.org/3/)  
- [Tkinter Library Guide](https://docs.python.org/3/library/tkinter.html)  
- [MySQL Documentation](https://dev.mysql.com/doc/)
