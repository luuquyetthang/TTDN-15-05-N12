from odoo import models, fields, api

class DanhMucLoaiXe(models.Model):
    _name = "loai_xe"
    _description = "Danh mục xe"

    name = fields.Char(string="Tên danh mục", required=True)
    description = fields.Char(string="Mô tả")
    phuong_tien_ids = fields.One2many('phuong_tien', 'loai_xe_id', string="Danh sách phương tiện")

    # Tạo trường đếm số lượng phương tiện
    phuong_tien_count = fields.Integer(string="Số lượng xe", compute="_compute_phuong_tien_count")

    @api.depends('phuong_tien_ids')
    def _compute_phuong_tien_count(self):
        for record in self:
            record.phuong_tien_count = len(record.phuong_tien_ids)
