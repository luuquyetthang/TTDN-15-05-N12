from odoo import models, fields

class FleetGPS(models.Model):
    _name = "vi_tri"
    _description = "Theo dõi GPS của xe"

    vehicle_id = fields.Many2one('phuong_tien', string="Phương Tiện", required=True)  # Xe được theo dõi GPS
    latitude = fields.Float(string="Vĩ độ")  # Vĩ độ
    longitude = fields.Float(string="Kinh độ")  # Kinh độ
    timestamp = fields.Datetime(string="Thời gian cập nhật vị trí", default=fields.Datetime.now)  # Thời gian cập nhật vị trí
