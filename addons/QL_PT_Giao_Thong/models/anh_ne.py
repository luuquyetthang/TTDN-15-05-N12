from odoo import models, fields

class AnhPhuongTien(models.Model):
    _name = "anh_ne"
    _description = "Ảnh phương tiện"

    image = fields.Binary(string="Ảnh", attachment=True, required=True)
    phuong_id = fields.Many2one('phuong_tien', string="Phương tiện", ondelete='cascade', required=True)
