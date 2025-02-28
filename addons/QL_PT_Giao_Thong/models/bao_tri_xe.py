from odoo import models, fields, api

class FleetMaintenance(models.Model):
    _name = "bao_tri_xe"
    _description = "Bảo dưỡng xe"

    vehicle_id = fields.Many2one('phuong_tien', string="Phương tiện", required=True)  # Xe được bảo trì
    ngay_bat_dau = fields.Date(string="Ngày bắt đầu")
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)  # Ngày bảo trì
    description = fields.Text(string="Miêu tả")  # Mô tả công việc bảo trì
    cost = fields.Float(string="Trị giá")  # Chi phí bảo trì
    next_ngay_ket_thuc = fields.Date(string="Ngày bảo trì tiếp theo")  # Ngày bảo trì tiếp theo

    @api.onchange('ngay_ket_thuc')
    def _compute_next_maintenance(self):
        if self.ngay_ket_thuc:
            self.next_ngay_ket_thuc = fields.Date.add(self.ngay_ket_thuc, months=6)  # Đặt lịch bảo trì tiếp theo sau 6 tháng
