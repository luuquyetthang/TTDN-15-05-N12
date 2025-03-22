from odoo import models, fields, api
from odoo.exceptions import ValidationError

class dondangky(models.Model):
    _name = "don_dang_ky"
    _description = "Đơn xin đăng ký làm tài xế"

    ten_don_dk = fields.Char(string="Tên đơn")
    name = fields.Char(string="Tên đầy đủ", required=True) 
    license_number = fields.Char(string="Số giấy phép", required=True)   
    phone = fields.Char(string="Phone") 
    tai_xe_id = fields.Many2one('tai_xe', string="Tài xế") 
    ngay_dang_ky = fields.Date(string="Ngày đăng ký", default=fields.Date.today)
    can_cuoc = fields.Integer(string="Căn cước công dân")
    ghi_chu = fields.Text(string="Ghi chú")
    hinh_tai_xe = fields.Image(string="Ảnh tài xế")
    hinh_giay_phep_truoc = fields.Image(string="Ảnh giấy phép (Mặt trước)")
    hinh_giay_phep_sau = fields.Image(string="Ảnh giấy phép (Mặt sau)")
    hinh_can_cuoc_truoc = fields.Image(string="Ảnh căn cước (Mặt trước)")
    hinh_can_cuoc_sau = fields.Image(string="Ảnh căn cước (Mặt sau)")
  

    saved_tai_xe_name = fields.Char(string="Tên tài xế ")
    saved_license_number = fields.Char(string="Số giấy phép")
    saved_phone = fields.Char(string="SĐT tài xế đã lưu")
    saved_can_cuoc = fields.Integer(string="Căn cước tài xế ")

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
        for record in self:
            if record.tai_xe_id:
                
                record.saved_tai_xe_name = record.tai_xe_id.name
                record.saved_license_number = record.tai_xe_id.license_number
                record.saved_phone = record.tai_xe_id.phone
                record.saved_can_cuoc = record.tai_xe_id.can_cuoc

                record.tai_xe_id.unlink()
                record.tai_xe_id = False

    def action_duyet(self):
        self.write({'trang_thai': 'duyet'})
        for record in self:
            if not record.tai_xe_id:
       
                tai_xe = self.env['tai_xe'].create({
                    'name': record.name,
                    'license_number': record.license_number,
                    'phone': record.phone,
                    'can_cuoc': record.can_cuoc,
                    'trang_thai': 'duyet',
                    'hinh_tai_xe': record.hinh_tai_xe,
                    'hinh_giay_phep_truoc': record.hinh_giay_phep_truoc,
                    'hinh_giay_phep_sau': record.hinh_giay_phep_sau,
                    'hinh_can_cuoc_truoc': record.hinh_can_cuoc_truoc,
                    'hinh_can_cuoc_sau': record.hinh_can_cuoc_sau,
                })
                record.tai_xe_id = tai_xe.id
            else:
               
                record.tai_xe_id.write({
                    'trang_thai': 'duyet',
                    'hinh_tai_xe': record.hinh_tai_xe,
                    'hinh_giay_phep_truoc': record.hinh_giay_phep_truoc,
                    'hinh_giay_phep_sau': record.hinh_giay_phep_sau,
                    'hinh_can_cuoc_truoc': record.hinh_can_cuoc_truoc,
                    'hinh_can_cuoc_sau': record.hinh_can_cuoc_sau,
                })

    def action_huy(self):
        self.write({'trang_thai': 'huy'})
        for record in self:
            if record.tai_xe_id:
                record.tai_xe_id.write({'trang_thai': 'huy'}) 
                record.tai_xe_id.unlink()
                record.tai_xe_id = False
