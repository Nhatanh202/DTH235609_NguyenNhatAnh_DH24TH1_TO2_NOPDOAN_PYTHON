from tkinter import messagebox
import tkinter as tk
from modules.data import load_data
from modules.crud import insert_record, update_record, delete_record, search_records, insert_hoa_don, generate_mahd


def lam_moi_bang(app, ten_bang, cot):
    """Tải lại dữ liệu cho bảng"""
    # clear tree
    tree = getattr(app, 'current_tree', None)
    if tree is None:
        return
    for r in tree.get_children():
        tree.delete(r)
    data = load_data(ten_bang)
    for idx, row in enumerate(data):
        tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=row, tags=(tag,))


def khi_them(app, ten_bang, cot):
    """Xử lý thêm bản ghi mới"""
    vals = app.get_form_values(cot)
    if ten_bang == 'HoaDon':
        vals[0] = generate_mahd()  # Luôn generate MaHD mới
        # Set back to form
        mahd_ent = app.form_entries.get('MaHD')
        if mahd_ent:
            mahd_ent.config(state='normal')
            mahd_ent.delete(0, tk.END)
            mahd_ent.insert(0, vals[0])
            mahd_ent.config(state='readonly')
    elif not vals[0]:
        # allow user to enter primary key; if empty warn
        messagebox.showwarning('Lỗi', 'Mã (khóa chính) không được để trống')
        return
    # Validate data
    if not validate_data(app, ten_bang, cot, vals, is_insert=True):
        return
    data = dict(zip(cot, vals))
    if ten_bang == 'HoaDon':
        ok = insert_hoa_don(data)
        if ok:
            lam_moi_bang(app, ten_bang, cot)
            # Also refresh XeMay table if visible
            if hasattr(app, 'current_table') and app.current_table == 'XeMay':
                xemay_columns = app.table_configs['XeMay']['cols']
                lam_moi_bang(app, 'XeMay', xemay_columns)
        else:
            messagebox.showerror('Lỗi', 'Không thể thêm hóa đơn. Lỗi cơ sở dữ liệu.')
    else:
        ok = insert_record(ten_bang, data)
        if ok:
            messagebox.showinfo('Thành công', f'Đã thêm {ten_bang} thành công!')
            lam_moi_bang(app, ten_bang, cot)
        else:
            messagebox.showerror('Lỗi', f'Không thể thêm {ten_bang}. Lỗi cơ sở dữ liệu.')


def khi_sua(app, ten_bang, cot):
    """Xử lý cập nhật bản ghi"""
    if ten_bang == 'HoaDon':
        messagebox.showinfo('Thông báo', 'Chức năng sửa hóa đơn hiện không được hỗ trợ để đảm bảo toàn vẹn dữ liệu.')
        return

    vals = app.get_form_values(cot)
    if not vals[0]:
        messagebox.showwarning('Lỗi', 'Chọn hoặc nhập Mã để sửa')
        return
    # Validate data (skip primary key)
    if not validate_data(app, ten_bang, cot[1:], vals[1:]):
        return
    data = dict(zip(cot[1:], vals[1:]))
    where_clause = f"{cot[0]} = ?"
    where_params = (vals[0],)
    ok = update_record(ten_bang, data, where_clause, where_params)
    if ok:
        messagebox.showinfo('Thành công', f'Đã cập nhật {ten_bang} thành công!')
        lam_moi_bang(app, ten_bang, cot)
        # Nếu sửa Xe máy, làm mới luôn bảng Hóa đơn nếu đang mở
        if ten_bang == 'XeMay' and hasattr(app, 'current_table') and app.current_table == 'HoaDon':
            hoadon_columns = app.table_configs['HoaDon']['cols']
            lam_moi_bang(app, 'HoaDon', hoadon_columns)
    else:
        messagebox.showerror('Lỗi', f'Không thể cập nhật {ten_bang}. Lỗi cơ sở dữ liệu.')


def khi_xoa(app, ten_bang, cot):
    """Xử lý xóa bản ghi"""
    if ten_bang == 'HoaDon':
        messagebox.showinfo('Thông báo', 'Chức năng xóa hóa đơn hiện không được hỗ trợ để đảm bảo toàn vẹn dữ liệu.')
        return

    pk = cot[0]
    pkval = app.form_entries[pk].get().strip()
    if not pkval:
        messagebox.showwarning('Lỗi', 'Chọn hoặc nhập Mã để xóa')
        return
    
    # Kiểm tra xem bản ghi có đang được tham chiếu trong bảng HoaDon không
    if ten_bang == 'XeMay':
        if check_exists_in_hoadon('MaXe', pkval):
            messagebox.showerror('Lỗi', f'Không thể xóa xe máy có mã {pkval} vì nó đã được ghi trong một hóa đơn.')
            return

    if not messagebox.askyesno('Xác nhận', f'Bạn có chắc muốn xóa {pkval}?'):
        return
    where_clause = f"{pk} = ?"
    where_params = (pkval,)
    ok = delete_record(ten_bang, where_clause, where_params)
    if ok:
        messagebox.showinfo('Thành công', f'Đã xóa {ten_bang} thành công!')
        lam_moi_bang(app, ten_bang, cot)
    else:
        messagebox.showerror('Lỗi', f'Không thể xóa {ten_bang}. Lỗi cơ sở dữ liệu hoặc do ràng buộc khóa ngoại.')


def khi_tim_kiem(app, ten_bang, cot, term):
    """Xử lý tìm kiếm"""
    tree = getattr(app, 'current_tree', None)
    if tree is None:
        return
    for r in tree.get_children():
        tree.delete(r)
    if not term:
        lam_moi_bang(app, ten_bang, cot)
        return
    rows = search_records(ten_bang, cot, term)
    for row in rows:
        tree.insert('', tk.END, values=row)


def validate_data(app, ten_bang, cot, vals, is_insert=False):
    """Validate dữ liệu đầu vào"""
    for i, col in enumerate(cot):
        val = vals[i]
        if ten_bang == 'HoaDon':
            # Bỏ qua kiểm tra các trường tự động khi thêm mới
            if is_insert and col in ['MaHD', 'GiaBan', 'TongThanhTien']:
                continue
        
        if ten_bang == 'HoaDon' and col == 'MaHD':
            continue  # MaHD is auto-generated
        if not val:
            # Cho phép TongThanhTien trống vì nó sẽ được tính toán
            if ten_bang == 'HoaDon' and col == 'TongThanhTien':
                continue
            messagebox.showwarning('Lỗi', f'{col} không được để trống')
            return False
        if col in ['GiaNhap', 'GiaBan']:
            # Bỏ qua kiểm tra GiaBan cho HoaDon vì nó được điền tự động
            if ten_bang == 'HoaDon' and col == 'GiaBan':
                continue
            if not val.isdigit() or int(val) <= 0:
                messagebox.showwarning('Lỗi', f'{col} phải là số dương')
                return False
        elif col == 'SoLuong':
            if not val.isdigit() or int(val) < 0:
                messagebox.showwarning('Lỗi', f'{col} phải là số không âm')
                return False
        elif col in ['SDT']:
            if val and not val.isdigit():
                messagebox.showwarning('Lỗi', f'{col} phải là số')
                return False
        # Check foreign keys for HoaDon
        if ten_bang == 'HoaDon':
            if col == 'MaNV':
                if not check_exists('NhanVien', 'MaNV', val):
                    messagebox.showwarning('Lỗi', f'Mã nhân viên {val} không tồn tại')
                    return False
            elif col == 'MaKH':
                if not check_exists('KhachHang', 'MaKH', val):
                    messagebox.showwarning('Lỗi', f'Mã khách hàng {val} không tồn tại')
                    return False
            elif col == 'MaXe':
                if not check_exists('XeMay', 'MaXe', val):
                    messagebox.showwarning('Lỗi', f'Mã xe {val} không tồn tại')
                    return False
    return True


def check_exists_in_hoadon(column, value):
    """Kiểm tra giá trị có tồn tại trong bảng HoaDon không"""
    data = load_data('HoaDon')
    # Lấy index của cột từ TABLE_CONFIGS
    try:
        from modules.constants import TABLE_CONFIGS
        col_index = TABLE_CONFIGS['HoaDon']['cols'].index(column)
    except (ImportError, ValueError):
        return False # Hoặc xử lý lỗi một cách phù hợp

    for row in data:
        if len(row) > col_index and str(row[col_index]) == str(value):
            return True
    return False


def check_exists(table, column, value):
    """Kiểm tra giá trị có tồn tại trong bảng không"""
    data = load_data(table)
    for row in data:
        if str(row[0]) == str(value):  # Assuming first column is key
            return True
    return False