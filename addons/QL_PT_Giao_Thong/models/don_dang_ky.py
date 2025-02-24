from odoo import models, fields, api

class dondangky(models.Model):
    _name = "don_dang_ky"
    _description = "Đơn xin đăng ký làm tài xế"

    tai_xe_id = fields.Many2one('tai_xe', string="Tài xế", required=True)
    ngay_dang_ky = fields.Date(string="Ngày đăng ký", default=fields.Date.today)
    can_cuoc = fields.Integer(string="Căn cước công dân")
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối')
    ], string="Trạng thái", default='cho_duyet')
    ghi_chu = fields.Text(string="Ghi chú")

    @api.model
    def create(self, vals):
        """Gửi thông báo khi có đơn đăng ký mới"""
        record = super(dondangky, self).create(vals)
        # Tùy chỉnh logic gửi thông báo nếu cần
        return record
# Ràng buộc: Một nhân viên chỉ có thể đăng ký 1 đơn đang chờ duyệt
    _sql_constraints = [
        ('unique_don_cho_duyet', 'UNIQUE(nhan_vien_id, trang_thai,can_cuoc)',
         'Mỗi nhân viên chỉ có thể có một đơn "Chờ duyệt"!')
    ]