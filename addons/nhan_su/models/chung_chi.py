from odoo import models, fields, api

class chungchi(models.Model):
    _name = 'chung.chi'
    _description = 'Quản lý Văn Bằng'

    name = fields.Char(string="Tên Văn Bằng", required=True)
    so_hieu = fields.Char(string="Số Hiệu")
    ngay_cap = fields.Date(string="Ngày Cấp")
    noi_cap = fields.Char(string="Nơi Cấp")
    loai_van_bang = fields.Selection([
        ('daihoc', 'Đại Học'),
        ('caodang', 'Cao Đẳng'),
        ('trungcap', 'Trung Cấp'),
        ('khac', 'Khác')
    ], string="Loại Văn Bằng", required=True)

    # Liên kết với bảng nhân viên
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân Viên", ondelete="cascade")

    # Lấy thông tin từ bảng nhân viên
    ma_dinh_danh = fields.Char(string="Mã Định Danh", related="nhan_vien_id.ma_dinh_danh", store=True, readonly=True)
    ho_va_ten = fields.Char(string="Họ và Tên", related="nhan_vien_id.ho_va_ten", store=True, readonly=True)
    ngay_sinh = fields.Date(string="Ngày Sinh", related="nhan_vien_id.ngay_sinh", store=True, readonly=True)
    que_quan = fields.Char(string="Quê Quán", related="nhan_vien_id.que_quan", store=True, readonly=True)
    email = fields.Char(string="Email", related="nhan_vien_id.email", store=True, readonly=True)
    so_dien_thoai = fields.Char(string="Số Điện Thoại", related="nhan_vien_id.so_dien_thoai", store=True, readonly=True)
