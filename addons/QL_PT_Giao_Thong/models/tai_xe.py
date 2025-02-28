from odoo import api, models, fields
from odoo.exceptions import ValidationError

class TaiXe(models.Model):
    _name = "tai_xe"
    _description = "Quản lý tài xế"

    name = fields.Char(string="Tên đầy đủ", required=True)  # Họ và tên tài xế
    license_number = fields.Char(string="Số giấy phép", required=True)  # Số giấy phép lái xe
    phone = fields.Char(string="Phone")  # Số điện thoại
    assigned_vehicle = fields.One2many('phuong_tien', 'driver_id', string="Xe được chỉ định")  # Xe đang lái
    don_dang_ky_ids = fields.One2many('don_dang_ky', 'tai_xe_id', string="Đơn đăng ký")
    lich_su_xe_ids = fields.One2many('lich_su_xe', 'tai_xe_id', string="Tài xế")
    
    @api.constrains('tai_xe_id')
    def _check_unique_don_dang_ky(self):
        for record in self:
            existing = self.search([('tai_xe_id', '=', record.tai_xe_id.id), ('id', '!=', record.id)])
            if existing:
                raise ValidationError("Mỗi tài xế chỉ có thể có một đơn đăng ký!")
            
    @api.depends('don_dang_ky_ids.trang_thai')
    def _compute_trang_thai(self):
        for record in self:
            trang_thai_list = record.don_dang_ky_ids.mapped('trang_thai')

            if 'duyet' in trang_thai_list:
                record.trang_thai = 'duyet'
            elif 'huy' in trang_thai_list:
                record.trang_thai = 'huy'
            else:
                record.trang_thai = 'cho_duyet'

    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('huy', 'Đã hủy')
    ], string="Trạng thái", compute="_compute_trang_thai", store=True)