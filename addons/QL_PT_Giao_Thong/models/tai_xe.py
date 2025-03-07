from odoo import api, models, fields


class TaiXe(models.Model):
    _name = "tai_xe"
    _description = "Quản lý tài xế"

    chuyen_di = fields.One2many('phuong_tien', 'driver_id', string="Xe được chỉ định")
    don_dang_ky_ids = fields.One2many('don_dang_ky', 'tai_xe_id', string="Đơn đăng ký")
    lich_su_xe_ids = fields.One2many('lich_su_xe', 'tai_xe_id', string="Lịch sử lái xe")

    name = fields.Char(string="Tên đầy đủ", required=True)
    license_number = fields.Char(string="Số giấy phép", required=True)
    phone = fields.Char(string="Số điện thoại")
    can_cuoc = fields.Char(string="Căn cước công dân")
    
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('huy', 'Đã hủy')
    ], string="Trạng thái", default='cho_duyet')