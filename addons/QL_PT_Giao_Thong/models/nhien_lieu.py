from odoo import models, fields

class NhienLieu(models.Model):
    _name = "nhien_lieu"
    _description = "Quản lý nhiên liệu"

    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  
    date = fields.Date(string="Ngày", required=True)  
    liters = fields.Float(string="Lít")  
    cost = fields.Float(string="Giá")  
    odometer = fields.Float(string="Đồng hồ đo đường (km)")  
