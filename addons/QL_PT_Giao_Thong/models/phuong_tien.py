from odoo import models, fields

class PhuongTien(models.Model):
    _name = "phuong_tien"
    _description = "Danh mục phương tiện"

    name = fields.Char(string="Biển số xe", required=True)  # Biển số xe
    model = fields.Char(string="Model")  # Mẫu xe (ví dụ: Toyota Camry)
    manufacturer = fields.Char(string="Hãng sản xuất")  # Hãng sản xuất (Toyota, Honda, Ford...)
    year = fields.Integer(string="Năm sản xuất")  # Năm sản xuất
    status = fields.Selection([
        ('active', 'Sẵn sàng'),
        ('maintenance', 'Đang sử dụng'),
        ('inactive', 'Bảo trì')
    ], string="Trạng thái", default='active')  # Trạng thái xe
    driver_id = fields.Many2one('phuong_tien', string="Xe được giao")  # Liên kết với tài xế đang lái xe

    # Liên kết với bảng nhien_lieu (Nhiên liệu) và vi_tri (GPS)
    fuel_ids = fields.One2many('nhien_lieu', 'vehicle_id', string="Thông tin nhiên liệu")
    gps_ids = fields.One2many('vi_tri', 'vehicle_id', string="Thông tin GPS")
