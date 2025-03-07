from odoo import api, models, fields


class DonThueXe(models.Model):
    _name = "don_thue_xe"
    _description = "Quản lý khách thuê"

    name = fields.Char(string="Tên đầy đủ", required=True, tracking=True)  
    sdt_khach = fields.Char(string="Số điện thoại", tracking=True)  
    dia_chi = fields.Char(string="Địa chỉ", tracking=True) 
    can_cuoc = fields.Char(string="Số CCCD", tracking=True, unique=True)  
    ma_don = fields.Char(string="Mã đơn", required=True)
    khach_id = fields.Many2one('khach_thue', string="Khách thuê") 

    # Thêm các trường lưu lại thông tin tài xế khi xóa
    saved_khach_thue_name = fields.Char(string="Tên đầy đủ")
    saved_sdt_khach = fields.Char(string="Số điện thoại")
    saved_dia_chi = fields.Char(string="Địa chỉ")
    saved_can_cuoc = fields.Integer(string="Số CCCD")   

    xe = fields.Selection([
        ('motor','xe máy'),
        ('car','Ô tô'),
    ])
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('huy', 'Đã hủy')
    ], string="Trạng thái", default='cho_duyet', tracking=True)

    @api.model
    def create(self, vals):
        if 'trang_thai' not in vals:
            vals['trang_thai'] = 'cho_duyet'
        return super(DonThueXe, self).create(vals)

    def action_cho_duyet(self):
        self.write({'trang_thai': 'cho_duyet'})
        for record in self:
            if record.khach_id:

                record.saved_khach_thue_name = record.khach_id.name
                record.saved_sdt_khach = record.khach_id.sdt_khach
                record.saved_dia_chi = record.khach_id.dia_chi
                record.saved_can_cuoc = record.khach_id.can_cuoc

                record.khach_id.unlink()


                record.khach_id = False


    def action_duyet(self):
        self.write({'trang_thai': 'duyet'})
        for record in self:
            if not record.khach_id:
                khach_thue = self.env['khach_thue'].create({
                    'name': record.name,
                    'sdt_khach': record.sdt_khach,
                    'dia_chi': record.dia_chi,
                    'can_cuoc': record.can_cuoc,
                    'trang_thai': 'duyet',  
                })
                record.khach_id = khach_thue.id  
            else:
                record.khach_id.write({'trang_thai': 'duyet'})  

    def action_huy(self):
        self.write({'trang_thai': 'huy'})
        # Xóa tài xế nếu có
        for record in self:
            if record.khach_id:
                record.khach_id.write({'trang_thai': 'huy'}) 
                record.khach_id.unlink()
                record.khach_id = False  