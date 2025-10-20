# 🏍️ QUẢN LÝ XE MÁY (Motorbike Management System)

> Đồ án Chuyên đề Python (COS525) - Trường Đại học An Giang

## 🌟 TÓM TẮT DỰ ÁN

Đây là ứng dụng máy tính để bàn (Desktop Application) được xây dựng bằng **Python** nhằm cung cấp một công cụ trực quan và hiệu quả để **Quản lý thông tin xe máy** (Thêm, Sửa, Xóa, Lưu và Tìm kiếm). Ứng dụng sử dụng giao diện đồ họa **Tkinter** và lưu trữ dữ liệu bền vững bằng **MySQL**.

### Tính năng nổi bật

* **Hỗ trợ CRUD** đầy đủ (Create, Read, Update, Delete) cho dữ liệu xe máy.
* Giao diện người dùng **trực quan** và thân thiện, dễ dàng thao tác.
* Khả năng **Tìm kiếm** thông minh theo nhiều tiêu chí.
* Sử dụng thư viện **`tkcalendar`** để chọn ngày tháng tiện lợi.
---

## 🚀 ĐỘI NGŨ PHÁT TRIỂN

| # | Họ và tên | MSSV | Lớp |
| :-: | :--- | :--- | :--- |
| 1 | Nguyễn Nhất Anh | DH235609 | DH24TH1 |
| 2 | Phạm Hữu Huy | DH235665 | DH24TH1 |

**Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh

---

## ⚙️ CÔNG NGHỆ SỬ DỤNG

| Lĩnh vực | Công cụ/Thư viện | Mục đích chính |
| :--- | :--- | :--- |
| **Ngôn ngữ** | **Python** | Phát triển cốt lõi (Áp dụng OOP) |
| **Giao diện (GUI)** | **Tkinter** | Xây dựng giao diện Desktop (Native) |
| **Cơ sở dữ liệu** | **MySQL** | Hệ quản trị CSDL để lưu trữ dữ liệu |
| **Kết nối CSDL** | `mysql-connector-python` | Thao tác CRUD thông qua Python |
| **Thư viện** | `tkcalendar`, `pillow` | Chọn ngày, xử lý/hiển thị hình ảnh |
| **IDE Khuyến nghị** | Visual Studio Code / PyCharm | Môi trường phát triển |

---

## 📦 CẤU TRÚC THƯ MỤC

Cấu trúc dự án được tổ chức theo mô hình module, giúp dễ dàng quản lý và bảo trì code: 
```bash

QuanLyXeMay/
├── main.py                  # 🚀 File chính chạy ứng dụng & Xử lý giao diện Tkinter
│
├── database/
│   ├── connect.py           # Thiết lập kết nối CSDL (MySQL)
│   └── setup.sql            # Script SQL tạo DB & Bảng
│
├── modules/
│   ├── crud.py              # Các logic nghiệp vụ: Thêm, Sửa, Xóa, Tìm kiếm
│   └── utils.py             # Hàm tiện ích (Validate, Format,...)
│
├── assets/
│   ├── icons/               # Icon, hình ảnh giao diện
│   └── logo.png
│
├── README.md                # Mô tả dự án (File này)
└── requirements.txt         # Danh sách thư viện cần cài đặt






Cảm ơn bạn đã xem qua đồ án!
