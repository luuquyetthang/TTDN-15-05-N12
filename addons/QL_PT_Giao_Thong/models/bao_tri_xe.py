from odoo import models, fields, api

class BaoTriXe(models.Model):
    _name = "bao_tri_xe"
    _description = "Bảo dưỡng xe"

    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  # Xe được bảo trì
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu")
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)  # Ngày bảo trì
    description = fields.Text(string="Miêu tả")  # Mô tả công việc bảo trì
    cost = fields.Float(string="Trị giá")  # Chi phí bảo trì
    next_ngay_ket_thuc = fields.Date(string="Ngày bảo trì tiếp theo")  # Ngày bảo trì tiếp theo
    trang_thai = fields.Selection([
        ('da_xong', 'Đã xong'),
        ('dang_bao_tri', 'Đang bảo dưỡng')
    ], string="Trạng thái", default="dang_bao_tri", required=True)

    @api.model
    def create(self, vals):
        """ Khi tạo bảo trì, chuyển phương tiện sang trạng thái bảo trì """
        record = super(BaoTriXe, self).create(vals)
        if record.vehicle_id:
            record.vehicle_id.write({'status': 'xe_bao_tri'})  # Cập nhật trạng thái phương tiện
        return record

    @api.onchange('ngay_ket_thuc')
    def _compute_next_maintenance(self):
        """ Tự động tính ngày bảo trì tiếp theo sau 6 tháng """
        if self.ngay_ket_thuc:
            self.next_ngay_ket_thuc = fields.Date.add(self.ngay_ket_thuc, months=6)

    @api.model
    def create(self, vals):
        if 'trang_thai' not in vals:
            vals['trang_thai'] = 'dang_bao_tri'
        return super(BaoTriXe, self).create(vals)

    def action_dang_bao_tri(self):
        self.write({'trang_thai': 'dang_bao_tri'})

    def action_da_xong(self):
        self.write({'trang_thai': 'da_xong'})