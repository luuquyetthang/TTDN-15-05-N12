from odoo import models, fields, api

class PhuongTien(models.Model):
    _name = "phuong_tien"
    _description = "Danh mục phương tiện"

    image_ids = fields.One2many('anh_ne', 'phuong_id', string="Hình ảnh phương tiện")
    main_image = fields.Binary(string="Ảnh đại diện", compute="_compute_main_image", store=True)
    @api.depends('image_ids.image')
    def _compute_main_image(self):
        for record in self:
            record.main_image = record.image_ids[:1].image if record.image_ids else False
    name = fields.Char(string="Biển số xe", required=True)  
    model = fields.Char(string="Model") 
    manufacturer = fields.Char(string="Hãng sản xuất")  
    year = fields.Integer(string="Năm sản xuất")  
    phuong_tien_id = fields.Many2one('khach_thue',string="Khách thuê xe")
    status = fields.Selection([
        ('xe_chua_giao', 'Chưa hoạt động'),
        ('xe_da_giao', 'Đang hoạt động'),
        ('xe_bao_tri', 'Xe bảo dưỡng')
    ], string="Trạng thái", compute="_compute_status_from_maintenance",  default='xe_da_giao', required=True,store=True,index = True)  

    @api.model
    def create(self, vals):
        if 'driver_id' in vals and vals['driver_id']:
            vals['status'] = 'xe_da_giao'
        else:
            vals.setdefault('status', 'xe_chua_giao')  
        return super(PhuongTien, self).create(vals)

    def write(self, vals):
        res = super(PhuongTien, self).write(vals) 
        for record in self:
            
            if record.driver_id:
                super(PhuongTien, record).write({'status': 'xe_da_giao'})
                
            elif 'driver_id' in vals and not vals['driver_id']:
                super(PhuongTien, record).write({'status': 'xe_chua_giao'})
                
        return res
    
    def action_xe_da_giao(self):
        self.write({'status': 'xe_da_giao'})
    def action_xe_chua_giao(self):
        self.write({'status': 'xe_chua_giao'})
    def action_xe_bao_tri(self):
        self.write({'status': 'xe_bao_tri'})

    loai_xe_id = fields.Many2one('loai_xe', string="Loại xe")
    driver_id = fields.Many2one('tai_xe', string="Xe được giao")
    
    fuel_ids = fields.One2many('nhien_lieu', 'vehicle_id', string="Thông tin nhiên liệu")
    gps_ids = fields.One2many('vi_tri', 'vehicle_id', string="Thông tin GPS")
    lich_su_xe_ids = fields.One2many('lich_su_xe', 'vehicle_id', string="Lịch sử xe")
    chuyen_di_ids = fields.One2many('chuyen_di', 'vehicle_id', string="Chuyến đi của xe")
    bao_tri_ids = fields.One2many('bao_tri_xe','vehicle_id',string="Bảo trì xe")
    _sql_constraints = [
        ('unique_bien_so_xe', 'UNIQUE(name)', 'Biển số xe phải là duy nhất!'),
    ]
    
    @api.depends('bao_tri_ids.trang_thai', 'driver_id')
    def _compute_status_from_maintenance(self):
        for record in self:
            if any(bt.trang_thai == 'dang_bao_tri' for bt in record.bao_tri_ids):
                record.status = 'xe_bao_tri'
            elif any(bt.trang_thai == 'da_xong' for bt in record.bao_tri_ids):
                record.status = 'xe_da_giao'
            else:
                record.status = 'xe_chua_giao'
    