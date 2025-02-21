from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin nhân viên'

    ma = fields.Char("Mã định danh", required=True)
    ten = fields.Char("Tên định danh")
    chuc = fields.Char("Chức vụ")
    ngay = fields.Date("Ngày sinh")
    que = fields.Char("Quê quán")
    email = fields.Char("Email")
    sdt = fields.Char("Số điện thoại")
