from odoo import api, models, fields


class KhachThueXe(models.Model):
    _name = "khach_thue"
    _description = "Quản lý khách thuê"

    ten_khach = fields.Char(string="Tên đầy đủ", required=True)  
    sdt_khach = fields.Char(string="Số điện thoại khách")  
    dia_chi = fields.Char(string="Địa chỉ khách") 
    can_cuoc = fields.Char(string= "Số căn cước công dân")
    don_thue_xe_ids = fields.One2many('don_thue_xe','ten_khach_id',string='Đơn thuê xe')