# 🏍️ QUẢN LÝ XE MÁY (Motorbike Management System)

> Đồ án Chuyên đề Python (COS525) - Trường Đại học An Giang

## 🌟 TÓM TẮT DỰ ÁN

Đây là ứng dụng máy tính để bàn (Desktop Application) được xây dựng bằng **Python** nhằm cung cấp một công cụ trực quan và hiệu quả để **Quản lý thông tin xe máy** (Thêm, Sửa, Xóa, Lưu và Tìm kiếm). Ứng dụng sử dụng giao diện đồ họa **Tkinter** và lưu trữ dữ liệu bền vững bằng **MySQL**, đáp ứng các yêu cầu CRUD cơ bản của hệ thống quản lý dữ liệu.

### Mục tiêu

* [cite_start]Xây dựng thành công giao diện người dùng GUI bằng thư viện Tkinter [cite: 161-162].
* Thực hiện đầy đủ các thao tác nghiệp vụ **CRUD** (Create, Read, Update, Delete) đối với thông tin xe máy.
* [cite_start]Dữ liệu được lưu trữ ổn định trong MySQL Database[cite: 201].

---

## 🚀 ĐỘI NGŨ PHÁT TRIỂN

| # | Họ và tên | MSSV | Lớp |
| :-: | :--- | :--- | :--- |
| 1 | Nguyễn Nhất Anh | DH235609 | DH24TH1 |
| 2 | Phạm Hữu Huy | DH235665 | DH24TH1 |

**Giảng viên hướng dẫn:** ThS. Nguyễn Ngọc Minh

---

## ⚙️ CÔNG NGHỆ ÁP DỤNG

| Lĩnh vực | Công cụ/Thư viện | Mục đích chính |
| :--- | :--- | :--- |
| **Ngôn ngữ** | **Python** | Phát triển cốt lõi (Áp dụng Lập trình Hướng đối tượng) |
| **Giao diện (GUI)** | **Tkinter** | Xây dựng giao diện Desktop (Native) |
| **Cơ sở dữ liệu** | **MySQL** | Hệ quản trị CSDL để lưu trữ dữ liệu bền vững |
| **Kết nối CSDL** | `mysql-connector-python` | Thao tác CRUD thông qua Python |
| **Tiện ích** | `tkcalendar` | [cite_start]Hỗ trợ chọn ngày tháng năm thân thiện [cite: 210] |

---

## 📦 CẤU TRÚC THƯ MỤC DỰ ÁN

Cấu trúc dự án được tổ chức theo mô hình module để dễ dàng quản lý Logic và GUI:
Cấu trúc dự án được tổ chức theo mô hình **module**, giúp dễ dàng quản lý và bảo trì code:

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
```
----

## 🛠️ HƯỚNG DẪN CÀI ĐẶT VÀ KHỞI CHẠY

### 1. Yêu cầu Tiên quyết

* Đã cài đặt **Python 3.6+**.
* Đã cài đặt và khởi chạy **MySQL Server**.

### 2. Thiết lập Môi trường

Cài đặt các thư viện Python cần thiết bằng lệnh sau:

```bash
pip install -r requirements.txt
# Hoặc: pip install mysql-connector-python tkcalendar
