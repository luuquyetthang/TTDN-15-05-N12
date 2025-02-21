from odoo import models, fields

class FleetTrip(models.Model):
    _name = "chuyen_di"
    _description = "Quản lý chuyến đi"

    name = fields.Char(string="Tên chuyến đi", required=True)  # Tên chuyến đi
    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  # Xe sử dụng
    driver_id = fields.Many2one('tai_xe', string="Tài xế", required=True)  # Tài xế lái
    start_location = fields.Char(string="Start Location")  # Điểm xuất phát
    end_location = fields.Char(string="End Location")  # Điểm đến
    date = fields.Date(string="Ngày chuyến đi")  # Ngày đi
    status = fields.Selection([
        ('scheduled', 'Đã lên lịch'),  
        ('in_progress', 'Đang tiến hành'),  
        ('completed', 'Hoàn thành')  
    ], string="Trạng thái", default='scheduled')  # Trạng thái chuyến đi
