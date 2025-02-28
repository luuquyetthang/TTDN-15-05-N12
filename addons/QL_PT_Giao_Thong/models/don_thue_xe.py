from odoo import api, models, fields


class DonThueXe(models.Model):
    _name = "don_thue_xe"
    _description = "Quản lý khách thuê"

    ten_don = fields.Char(string="Tên đầy đủ")  
    ten_khach_id = fields.Many2one('khach_thue',string="Tên đầy đủ")   
    dia_chi_don = fields.Char(string="Địa chỉ đón khách") 
    xe = fields.Char(string="Loại xe và biển số") 
    