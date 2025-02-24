from odoo import models, fields

class TaiXe(models.Model):
    _name = "tai_xe"
    _description = "Quản lý tài xế"

    name = fields.Char(string="Tên đầy đủ", required=True)  # Họ và tên tài xế
    license_number = fields.Char(string="Số giấy phép", required=True)  # Số giấy phép lái xe
    phone = fields.Char(string="Phone")  # Số điện thoại
    assigned_vehicle = fields.One2many('phuong_tien', 'driver_id', string="Xe được chỉ định")  # Xe đang lái
    don_dang_ky_ids = fields.One2many('don_dang_ky', 'tai_xe_id', string="Đơn đăng ký")