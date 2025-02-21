from odoo import models,fields,api
class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Danh sách các phòng ban'

    ma_phong_ban = fields.Char("Mã Phòng Ban" ,required=True)
    ten_phong_ban = fields.Char("Tên Phòng Ban")