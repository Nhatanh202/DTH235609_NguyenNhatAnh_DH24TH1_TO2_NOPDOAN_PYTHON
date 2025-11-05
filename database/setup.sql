CREATE DATABASE QUANLYCUAHANGXEMAY
USE QUANLYCUAHANGXEMAY 

CREATE TABLE NhanVien (
	MaNV VARCHAR(10) PRIMARY KEY,       -- Khóa chính
    TenNV NVARCHAR(100) NOT NULL,       -- Dùng NVARCHAR cho tiếng Việt có dấu
	ChucVu NVARCHAR(50)                 -- Có thể bổ sung SDT, DiaChi, NgayVaoLam
);
CREATE TABLE KhachHang (
        MaKH VARCHAR(10) PRIMARY KEY,       -- Khóa chính
        TenKH NVARCHAR(100) NOT NULL,
        SDT VARCHAR(15),
        DiaChi NVARCHAR(255)
    );
 CREATE TABLE XeMay (
        MaXe VARCHAR(10) PRIMARY KEY,       -- Mã xe
        TenXe NVARCHAR(100) NOT NULL,       -- Tên xe
        LoaiXe NVARCHAR(20),                -- Xe số, Xe ga, Xe côn tay
        HangXe NVARCHAR(50),
        MauSac NVARCHAR(30),
        GiaNhap DECIMAL(12, 0) NOT NULL,
        GiaBan DECIMAL(12, 0),
        SoKhung VARCHAR(20) UNIQUE          -- Số khung duy nhất
    );
CREATE TABLE HoaDon (
        MaHD VARCHAR(10) PRIMARY KEY,       -- Mã hóa đơn
        NgayLap DATE,                       -- Ngày lập
        TongGiaTri DECIMAL(14, 2),          -- Tổng tiền

        -- Khóa ngoại
        MaNV VARCHAR(10),
        MaKH VARCHAR(10),
        MaXe VARCHAR(10),

        CONSTRAINT FK_HoaDon_NhanVien FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
        CONSTRAINT FK_HoaDon_KhachHang FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
        CONSTRAINT FK_HoaDon_XeMay FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe)
    );
CREATE TABLE ChiTietHoaDon(
    [MaHD]      VARCHAR(10) NOT NULL,
    [MaXe]      VARCHAR(10) NOT NULL,

    -- Thông tin giao dịch
    SoLuong INT         NOT NULL,
    ThanhTien DECIMAL(14, 2) NOT NULL,
	GiaBan DECIMAL(12, 0),
    -- Khóa chính kép (Composite Primary Key)
    PRIMARY KEY (MaHD, MaXe),

    -- Định nghĩa Khóa ngoại
    CONSTRAINT FK_ChiTietHD_HoaDon FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD),
    CONSTRAINT FK_ChiTietHD_XeMay FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe)
);
SELECT * FROM ChiTietHoaDon