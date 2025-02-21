from odoo import models, fields

class FleetFuel(models.Model):
    _name = "nhien_lieu"
    _description = "Quản lý nhiên liệu"

    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  # Xe tiêu thụ nhiên liệu
    date = fields.Date(string="Ngày", required=True)  # Ngày đổ nhiên liệu
    liters = fields.Float(string="Lít")  # Số lít nhiên liệu đã nạp
    cost = fields.Float(string="Giá")  # Chi phí nhiên liệu
    odometer = fields.Float(string="Đồng hồ đo đường (km)")  # Số km hiện tại của xe
