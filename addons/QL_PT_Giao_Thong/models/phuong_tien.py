from odoo import models, fields, api

class PhuongTien(models.Model):
    _name = "phuong_tien"
    _description = "Danh mục phương tiện"

    name = fields.Char(string="Biển số xe", required=True)  # Biển số xe
    loai_xe = fields.Selection([
        ('motor','xe máy'),
        ('car','Ô tô'),
    ])
    model = fields.Char(string="Model")  # Mẫu xe (ví dụ: Toyota Camry)
    manufacturer = fields.Char(string="Hãng sản xuất")  # Hãng sản xuất (Toyota, Honda, Ford...)
    year = fields.Integer(string="Năm sản xuất")  # Năm sản xuất
    status = fields.Selection([
        ('xe_chua_giao', 'Xe chưa giao'),
        ('xe_da_giao', 'Xe đã giao'),
        ('xe_bao_tri', 'Xe bảo trì')
    ], string="Trạng thái", default='xe_da_giao')  # Trạng thái xe

    @api.model
    def create(self, vals):
        if 'driver_id' in vals and vals['driver_id']:
            vals['status'] = 'xe_da_giao'
        else:
            vals.setdefault('status', 'xe_chua_giao')  # Đặt mặc định nếu không có giá trị
        return super(PhuongTien, self).create(vals)

    def write(self, vals):
        res = super(PhuongTien, self).write(vals)  # Gọi super để cập nhật dữ liệu trước
        for record in self:
            # Nếu có tài xế, đặt trạng thái là 'xe_da_giao'
            if record.driver_id:
                super(PhuongTien, record).write({'status': 'xe_da_giao'})
            # Nếu tài xế bị xóa (driver_id = False), đặt trạng thái về 'xe_chua_giao'
            elif 'driver_id' in vals and not vals['driver_id']:
                super(PhuongTien, record).write({'status': 'xe_chua_giao'})

        return res
    def action_xe_da_giao(self):
        self.write({'status': 'xe_da_giao'})
    def action_xe_chua_giao(self):
        self.write({'status': 'xe_chua_giao'})
    def action_xe_bao_tri(self):
        self.write({'status': 'xe_bao_tri'})

    driver_id = fields.Many2one('tai_xe', string="Xe được giao")  # Liên kết với tài xế đang lái xe

    # Liên kết với bảng nhien_lieu (Nhiên liệu) và vi_tri (GPS)
    fuel_ids = fields.One2many('nhien_lieu', 'vehicle_id', string="Thông tin nhiên liệu")
    gps_ids = fields.One2many('vi_tri', 'vehicle_id', string="Thông tin GPS")
    lich_su_xe_ids = fields.One2many('lich_su_xe', 'vehicle_id', string="Lịch sử xe")
# Đảm bảo tính duy nhất bằng SQL Constraint
    _sql_constraints = [
        ('unique_bien_so_xe', 'UNIQUE(name)', 'Biển số xe phải là duy nhất!'),
    ]