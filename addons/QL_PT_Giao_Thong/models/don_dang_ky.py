from odoo import models, fields, api
from odoo.exceptions import ValidationError

class dondangky(models.Model):
    _name = "don_dang_ky"
    _description = "Đơn xin đăng ký làm tài xế"

    name = fields.Char(string="Tên đơn")
    tai_xe_id = fields.Many2one('tai_xe', string="Tài xế", required = True) 
    ngay_dang_ky = fields.Date(string="Ngày đăng ký", default=fields.Date.today)
    can_cuoc = fields.Integer(string="Căn cước công dân")
    ghi_chu = fields.Text(string="Ghi chú")

    @api.constrains('tai_xe_id')
    def _check_unique_don_dang_ky(self):
        for record in self:
            existing = self.search([('tai_xe_id', '=', record.tai_xe_id.id), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Mỗi tài xế chỉ có thể có một đơn đăng ký!")
    # Trạng thái có 3 lựa chọn, mặc định là "Chờ duyệt"
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('huy', 'Đã hủy')
    ], string="Trạng thái", default='cho_duyet', tracking=True)

    @api.model
    def create(self, vals):
        if 'trang_thai' not in vals:
            vals['trang_thai'] = 'cho_duyet'
        return super(dondangky, self).create(vals)

    def action_cho_duyet(self):
        self.write({'trang_thai': 'cho_duyet'})

    def action_duyet(self):
        self.write({'trang_thai': 'duyet'})

    def action_huy(self):
        self.write({'trang_thai': 'huy'})
# Ràng buộc: Một nhân viên chỉ có thể đăng ký 1 đơn đang chờ duyệt
    _sql_constraints = [
        ('unique_don_cho_duyet', 'UNIQUE(tai_xe_id, trang_thai)',
         'Mỗi nhân viên chỉ có thể có một đơn "Chờ duyệt"!')
    ]