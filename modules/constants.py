# Theme colors for a motorcycle shop look
MAU_CHINH = "#105d3b"  # Màu chính (xanh lá)
MAU_PHU = "#436007"    # Màu phụ (xanh lục)
MAU_NEN = '#f4f7fa'   # Màu nền
MAU_BANG = '#ffffff'  # Màu bảng
MAU_CHU = "#000000"   # Màu chữ

# Table configurations
TABLE_CONFIGS = {
    'NhanVien': {
        'cols': ('MaNV', 'HoLot', 'TenNV', 'Phai', 'NgaySinh', 'ChucVu'),
        'heads': ('Mã NV', 'Họ lót', 'Tên', 'Phái', 'Ngày sinh', 'Chức vụ')
    },
    'KhachHang': {
        'cols': ('MaKH', 'TenKH', 'SDT', 'DiaChi'),
        'heads': ('Mã KH', 'Tên KH', 'SĐT', 'Địa chỉ')
    },
    'XeMay': {
        'cols': ('MaXe', 'TenXe', 'LoaiXe', 'HangXe', 'GiaNhap', 'GiaBan', 'SoLuong'),
        'heads': ('Mã xe', 'Tên xe', 'Loại xe', 'Hãng xe', 'Giá nhập', 'Giá bán', 'Số lượng')
    },
    'HoaDon': {
        'cols': ('MaHD', 'NgayLap', 'MaNV', 'MaKH', 'MaXe', 'SoLuong', 'GiaBan', 'TongThanhTien'),
        'heads': ('Mã HD', 'Ngày lập', 'Mã NV', 'Mã KH', 'Mã xe', 'SL', 'Giá bán', 'Tổng tiền')
    }
}