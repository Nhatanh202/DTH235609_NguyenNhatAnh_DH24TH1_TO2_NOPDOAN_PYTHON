-- 1. Sử dụng CSDL (Giả định CSDL QUANLYCUAHANGXEMAY đã tồn tại)
CREATE DATABASE QUANLYCUAHANGXEMAY;
GO
USE QUANLYCUAHANGXEMAY;
GO

CREATE TABLE [dbo].[TaiKhoan] (
    [TenDangNhap] VARCHAR(50) PRIMARY KEY,
    [MatKhau]     VARCHAR(255) NOT NULL, 
 );
GO
-----------------------------------------------------------------
-- 2. TẠO CÁC BẢNG MASTER (XeMay, NhanVien, KhachHang) - ĐÃ CẬP NHẬT
-----------------------------------------------------------------

-- 2.1. Bảng NHANVIEN (Đã thêm HoLot và Phai)
CREATE TABLE [dbo].[NhanVien] (
    [MaNV]        VARCHAR(10) PRIMARY KEY,
	[HoLot]       NVARCHAR(50)  NULL, -- Cột mới
    [TenNV]       NVARCHAR(100) NOT NULL,
	[Phai]        NVARCHAR(5)   NULL, -- Cột mới
	[NgaySinh]    DATE          NULL,
    [ChucVu]      NVARCHAR(50)  NULL,
);
GO

-- 2.2. Bảng KHACHHANG (Không đổi)
CREATE TABLE [dbo].[KhachHang] (
    [MaKH]        VARCHAR(10) PRIMARY KEY,
    [TenKH]       NVARCHAR(100) NOT NULL,
    [SDT]         VARCHAR(15)   NULL,
    [DiaChi]      NVARCHAR(255) NULL
);
GO

-- 2.3. Bảng XEMAY (Đã thêm LoaiXe, GiaNhap, GiaBan, TinhTrang)
CREATE TABLE [dbo].[XeMay] (
    [MaXe]        VARCHAR(10) PRIMARY KEY,
    [TenXe]       NVARCHAR(100) NOT NULL,
    [LoaiXe]      NVARCHAR(20)  NULL,       -- Cột mới
    [HangXe]      NVARCHAR(50)  NULL,
    [MauSac]      NVARCHAR(30)  NULL,
    [GiaNhap]     DECIMAL(12, 0) NOT NULL,  -- Cột mới (Giả định là giá vốn)
    [GiaBan]      DECIMAL(12, 0) NULL,      -- Cột mới (Giá bán niêm yết/đề xuất)
    [SoKhung]     VARCHAR(20) UNIQUE,
    [TinhTrang]   NVARCHAR(50)  NULL DEFAULT N'Mới 100%' -- Cột mới
);
GO

-----------------------------------------------------------------
-- 3. TẠO BẢNG TRANSACTION (HOADON) - KHÔNG ĐỔI
-----------------------------------------------------------------

CREATE TABLE [dbo].[HoaDon] (
    [MaHD]        VARCHAR(10) PRIMARY KEY,
    [NgayLap]     DATE          NOT NULL,
	[MaNV]        VARCHAR(10)   NOT NULL,
    [MaKH]        VARCHAR(10)   NOT NULL,
    [MaXe]        VARCHAR(10)   NOT NULL UNIQUE,
	[SoLuong]	INT			NOT NULL,	
    [GiaBan] DECIMAL(12, 2) NOT NULL,
    [TongThanhTien] DECIMAL(14, 2) NOT NULL,
    
    CONSTRAINT FK_HoaDon_NhanVien FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    CONSTRAINT FK_HoaDon_KhachHang FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    CONSTRAINT FK_HoaDon_XeMay FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe)
);
GO



-----------------------------------------------------------------
-- 4. CHÈN DỮ LIỆU MẪU (ĐÃ CẬP NHẬT)
-----------------------------------------------------------------

PRINT N'--- Chèn dữ liệu Master ĐÃ CẬP NHẬT ---';
-- Dữ liệu NhanVien mới
INSERT INTO NhanVien (MaNV, TenNV, HoLot, Phai, ChucVu, NgaySinh) VALUES
('NV001', N'Anh', N'Nguyễn Nhất', N'Nam', N'Quản lý', '2000-01-01'),
('NV002', N'Huy', N'Phạm Hữu', N'Nam', N'Bán hàng', '2000-02-02');

-- Dữ liệu KhachHang không đổi
INSERT INTO KhachHang (MaKH, TenKH, SDT, DiaChi) VALUES
('KH001', N'Trần Văn A', '090111222', N'An Giang'),
('KH002', N'Lê Thị B', '090222333', N'Cần Thơ');

-- Dữ liệu XeMay mới
INSERT INTO XeMay (MaXe, TenXe, LoaiXe, HangXe, MauSac, GiaNhap, GiaBan, SoKhung, TinhTrang) VALUES
('XM001', N'Vision', N'Xe ga', N'Honda', N'Đỏ', 25000000, 30000000, 'VIN12345', N'Mới 100%'),
('XM002', N'Exciter 155', N'Xe côn', N'Yamaha', N'Xanh', 40000000, 48000000, 'VIN67890', N'Mới 100%');
GO

PRINT N'--- Chèn dữ liệu Hóa Đơn ---';
INSERT INTO HoaDon (MaHD, NgayLap, GiaBan, TongThanhTien, MaNV, MaKH, MaXe, SoLuong) VALUES
('HD001', '2024-05-10', 30000000,  30000000, 'NV002', 'KH001', 'XM001', 1),
('HD002', '2024-05-11', 47000000,  46060000, 'NV001', 'KH002', 'XM002', 2);
GO

PRINT N'--- Tạo CSDL và chèn dữ liệu mẫu thành công! ---';
GO

SELECT * FROM XeMay
SELECT * FROM NhanVien
SELECT * FROM KhachHang
SELECT * FROM HoaDon
