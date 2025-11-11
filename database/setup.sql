USE QUANLYCUAHANGXEMAY;
GO

CREATE TABLE [dbo].[NhanVien] (
	[MaNV]        VARCHAR(10) PRIMARY KEY,
    [TenNV]       NVARCHAR(100) NOT NULL,
	[ChucVu]      NVARCHAR(50)  NULL,
    [HoLot]       NVARCHAR(50)  NULL,
    [Phai]        NVARCHAR(5)   NULL,
    [NgaySinh]    DATE          NULL
);
GO

-- 2.2. Bảng KHACHHANG
CREATE TABLE [dbo].[KhachHang] (
    [MaKH]        VARCHAR(10) PRIMARY KEY,
    [TenKH]       NVARCHAR(100) NOT NULL,
    [SDT]         VARCHAR(15)   NULL,
    [DiaChi]      NVARCHAR(255) NULL
);
GO

-- 2.3. Bảng XEMAY (Đã thêm TinhTrang)
CREATE TABLE [dbo].[XeMay] (
    [MaXe]        VARCHAR(10) PRIMARY KEY,
    [TenXe]       NVARCHAR(100) NOT NULL,
    [LoaiXe]      NVARCHAR(20)  NULL,
    [HangXe]      NVARCHAR(50)  NULL,
    [MauSac]      NVARCHAR(30)  NULL,
    [GiaNhap]     DECIMAL(12, 0) NOT NULL, 
    [GiaBan]      DECIMAL(12, 0) NULL,     
    [SoKhung]     VARCHAR(20) UNIQUE,
    [TinhTrang]   NVARCHAR(50)  NULL DEFAULT N'Mới 100%' -- Thêm TinhTrang
);
GO

-- 2.4. Bảng HOADON (Header - Đã loại bỏ MaXe)
CREATE TABLE [dbo].[HoaDon] (
    [MaHD]        VARCHAR(10) PRIMARY KEY,
    [NgayLap]     DATE          NULL,
    [TongGiaTri]  DECIMAL(14, 2) NULL, 
    [MaNV]        VARCHAR(10)   NULL,
    [MaKH]        VARCHAR(10)   NULL,

    CONSTRAINT FK_HoaDon_NhanVien FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    CONSTRAINT FK_HoaDon_KhachHang FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH)
);
GO

-- 2.5. Bảng CHITIETHD (Chi Tiết Hóa Đơn)
CREATE TABLE [dbo].[ChiTietHD] (
    [MaHD]      VARCHAR(10) NOT NULL,
    [MaXe]      VARCHAR(10) NOT NULL,
    [SoLuong]   INT         NOT NULL,
    [GiaBan]    DECIMAL(12, 2) NOT NULL, -- Giá bán thực tế
    [GiamGia]   DECIMAL(5, 2)  NULL DEFAULT 0, -- Giảm giá (ví dụ: 0.05 = 5%)
    [ThanhTien] DECIMAL(14, 2) NOT NULL,

    PRIMARY KEY (MaHD, MaXe),
    CONSTRAINT FK_ChiTietHD_HoaDon FOREIGN KEY (MaHD) REFERENCES HoaDon(MaHD),
    CONSTRAINT FK_ChiTietHD_XeMay FOREIGN KEY (MaXe) REFERENCES XeMay(MaXe)
);
GO

-----------------------------------------------------------------
-- 3. CHÈN DỮ LIỆU MẪU (Đúng thứ tự)
-----------------------------------------------------------------

-- 3.1. Chèn Bảng Cha (NhanVien, KhachHang, XeMay)
PRINT 'Đang chèn dữ liệu bảng Master...';
INSERT INTO NhanVien (MaNV, TenNV, ChucVu, HoLot, Phai, NgaySinh) VALUES
('NV001', N'Anh', N'Nguyễn Nhất', N'Nam', N'Quản lý', '2000-01-01'),
('NV002', N'Huy', N'Phạm Hữu', N'Nam', N'Bán hàng', '2000-02-02'),
('NV003', N'Minh', N'Nguyễn Ngọc', N'Nam', N'Kế toán', '1990-03-03');

INSERT INTO KhachHang (MaKH, TenKH, SDT, DiaChi) VALUES
('KH001', N'Trần Văn A', '090111222', N'An Giang'),
('KH002', N'Lê Thị B', '090222333', N'Cần Thơ'),
('KH003', N'Võ Văn C', '090333444', N'Đồng Tháp');

INSERT INTO XeMay (MaXe, TenXe, LoaiXe, HangXe, MauSac, GiaNhap, GiaBan, SoKhung, TinhTrang) VALUES
('XM001', N'Vision', N'Xe ga', N'Honda', N'Đỏ', 25000000, 30000000, 'VIN12345', N'Mới 100%'),
('XM002', N'Exciter 155', N'Xe côn', N'Yamaha', N'Xanh', 40000000, 48000000, 'VIN67890', N'Mới 100%'),
('XM003', N'Sirius FI', N'Xe số', N'Yamaha', N'Trắng', 18000000, 22000000, 'VIN55555', N'Đã qua sử dụng');
GO

/* LỆNH SAI (VÍ DỤ) */
INSERT INTO NhanVien (MaNV, TenNV, ChucVu,            HoLot,            Phai,   NgaySinh) 
VALUES
('NV001', N'Anh', N'Quản lý',      N'Nguyễn Nhất',  N'Nam', '2000-01-01'),
('NV002', N'Huy', N'Bán hàng',     N'Phạm Hữu',      N'Nam', '2000-02-02'),
('NV003', N'Minh', N'Kế toán',      N'Nguyễn Ngọc',   N'Nam', '1990-03-03'),
('NV004', N'Trang', N'Nhân viên Kho', N'Trần Thị',      N'Nữ',  '1998-10-15');
INSERT INTO NhanVien (MaNV, TenNV, ChucVu,        HoLot,           Phai,   NgaySinh)
VALUES       
('NV002', N'Huy', N'Bán hàng',     N'Phạm Hữu',      N'Nam', '2000-02-02'),
('NV003', N'Minh', N'Kế toán',      N'Nguyễn Ngọc',   N'Nam', '1990-03-03'),
('NV004', N'Trang', N'Nhân viên Kho', N'Trần Thị',      N'Nữ',  '1998-10-15');

-- 3.2. Chèn Bảng Con (HoaDon, ChiTietHD)
PRINT 'Đang chèn dữ liệu bảng Transaction...';
INSERT INTO HoaDon (MaHD, NgayLap, TongGiaTri, MaNV, MaKH) VALUES
('HD001', '2024-05-10', 70000000, 'NV002', 'KH001'),
('HD002', '2024-05-11', 48000000, 'NV001', 'KH003');

INSERT INTO ChiTietHD (MaHD, MaXe, SoLuong, GiaBan, GiamGia, ThanhTien) VALUES
('HD001', 'XM001', 1, 30000000, 0, 30000000), -- Hóa đơn 1, bán xe Vision
('HD001', 'XM003', 2, 20000000, 0, 40000000), -- Hóa đơn 1, bán 2 xe Sirius
('HD002', 'XM002', 1, 48000000, 0, 48000000);  -- Hóa đơn 2, bán xe Exciter
GO

PRINT 'Tạo CSDL và chèn dữ liệu mẫu thành công!';
GO

-- 4. KIỂM TRA DỮ LIỆU
SELECT * FROM NhanVien;
SELECT * FROM KhachHang;
SELECT * FROM XeMay;
SELECT * FROM HoaDon;
SELECT * FROM ChiTietHD;

/* 4. CHÈN DỮ LIỆU MẪU (BẮT BUỘC CHẠY TRƯỚC INSERT HOADON) */

-- Chèn 3 Nhân Viên (Khớp với MaNV trong INSERT HoaDon)
INSERT INTO NhanVien (MaNV, TenNV, ChucVu, HoLot, Phai, NgaySinh) VALUES
('NV001', N'Anh', N'Nguyễn Nhất', N'Nam', N'Quản lý', '2000-01-01'),
('NV002', N'Huy', N'Phạm Hữu', N'Nam', N'Bán hàng', '2000-02-02'),
('NV003', N'Minh', N'Nguyễn Ngọc', N'Nam', N'Kế toán', '1990-03-03');

-- Chèn 3 Khách Hàng (Khớp với MaKH trong INSERT HoaDon)
INSERT INTO KhachHang (MaKH, TenKH, SDT, DiaChi) VALUES
('KH001', N'Trần Văn A', '090111222', N'An Giang'),
('KH002', N'Lê Thị B', '090222333', N'Cần Thơ'),
('KH003', N'Võ Văn C', '090333444', N'Đồng Tháp');

-- Chèn Xe Máy (Để dùng cho ChiTietHoaDon)
INSERT INTO XeMay (MaXe, TenXe, LoaiXe, HangXe, MauSac, GiaNhap, GiaBan, SoKhung) VALUES
('XM001', N'Vision', N'Xe ga', N'Honda', N'Đỏ', 25000000, 30000000, 'VIN12345'),
('XM002', N'Exciter 155', N'Xe côn', N'Yamaha', N'Xanh', 40000000, 48000000, 'VIN67890');
GO

/* 5. CHÈN DỮ LIỆU HOADON (Bây giờ sẽ chạy thành công) */
INSERT INTO HoaDon (MaHD, NgayLap, TongGiaTri, MaNV, MaKH) VALUES
('HD001', '2024-05-10', NULL, 'NV002', 'KH001'),
('HD002', '2024-05-10', NULL, 'NV002', 'KH002'),
('HD003', '2024-05-11', NULL, 'NV001', 'KH001'),
('HD004', '2024-05-11', NULL, 'NV003', 'KH003');
GO

/* 6. CHÈN DỮ LIỆU CHITIETHOADON */
INSERT INTO ChiTietHoaDon (MaHD, MaXe, SoLuong, ThanhTien, GiaBan) VALUES
('HD001', 'XM001', 1, 30000000, 30000000),
('HD002', 'XM002', 1, 48000000, 48000000);
GO

/* 7. KIỂM TRA DỮ LIỆU */
SELECT * FROM NhanVien;
SELECT * FROM KhachHang;
SELECT * FROM XeMay;
SELECT * FROM HoaDon;
SELECT * FROM ChiTietHD;