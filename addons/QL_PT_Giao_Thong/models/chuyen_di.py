from odoo import models, fields

class FleetTrip(models.Model):
    _name = "chuyen_di"
    _description = "Quản lý chuyến đi"

    name = fields.Char(string="Tên chuyến đi", required=True)  
    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  
    driver_id = fields.Many2one('tai_xe', string="Tài xế", required=True)  
    start_location = fields.Char(string="Start Location")  
    end_location = fields.Char(string="End Location")  
    date = fields.Date(string="Ngày chuyến đi")  
    status = fields.Selection([
        ('scheduled', 'Đã lên lịch'),  
        ('in_progress', 'Đang tiến hành'),  
        ('completed', 'Hoàn thành')  
    ], string="Trạng thái", default='scheduled') 
