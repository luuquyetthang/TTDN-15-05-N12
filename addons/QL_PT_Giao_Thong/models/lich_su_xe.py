from odoo import fields,api,models

class LichSuXe(models.Model):
    _name = "lich_su_xe"
    _description = "Lịch sử xe"

    name = fields.Char(string="Mã lịch sử", required=True, copy=False, readonly=True, default=lambda self: 'New')
    vehicle_id = fields.Many2one('phuong_tien', string="Xe", required=True, help="Xe liên quan đến lịch sử này")
    ngay_su_dung = fields.Date(string="Ngày sử dụng", required=True, help="Ngày xe được sử dụng")
    km_bat_dau = fields.Float(string="Số km bắt đầu", help="Số km khi bắt đầu sử dụng")
    km_ket_thuc = fields.Float(string="Số km kết thúc", help="Số km khi kết thúc sử dụng")
    tai_xe_id = fields.Many2one('tai_xe', string="Người sử dụng", help="Người đã sử dụng xe")
    noi_dung_su_dung = fields.Text(string="Nội dung sử dụng", help="Chi tiết mục đích sử dụng xe")
    tinh_trang_xe = fields.Selection([
        ('tot', 'Tốt'),
        ('can_bao_duong', 'Cần bảo dưỡng'),
        ('hu_hong', 'Hư hỏng')
    ], string="Tình trạng xe", default="tot", help="Tình trạng của xe sau khi sử dụng")
    ngay_bao_duong = fields.Date(string="Ngày bảo dưỡng", help="Ngày xe được bảo dưỡng")
    ghi_chu = fields.Text(string="Ghi chú", help="Thông tin bổ sung về lịch sử xe")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('lich_su_xe') or 'New'
        return super(LichSuXe, self).create(vals)