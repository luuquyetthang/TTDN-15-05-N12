from odoo import api, models, fields


class KhachThueXe(models.Model):
    _name = "khach_thue"
    _description = "Quản lý khách thuê"

    name = fields.Char(string="Tên đầy đủ", required=True)
    sdt_khach = fields.Char(string="Số giấy phép", required=True)
    dia_chi = fields.Char(string="Số điện thoại")
    can_cuoc = fields.Char(string="Căn cước công dân")

    don_thue_xe_ids = fields.One2many('don_thue_xe', 'khach_id', string='Đơn thuê xe')
    khach_ids = fields.One2many('phuong_tien','phuong_tien_id', string="Phương tiện")
    trang_thai = fields.Selection([
        ('cho_duyet', 'Chờ duyệt'),
        ('duyet', 'Đã duyệt'),
        ('huy', 'Đã hủy')
    ], string="Trạng thái", default='cho_duyet')
    hinh_khach_thue = fields.Image(string="Ảnh khách thuê")
    hinh_can_cuoc_truoc = fields.Image(string="Ảnh căn cước (Mặt trước)")
    hinh_can_cuoc_sau = fields.Image(string="Ảnh căn cước (Mặt sau)")
    hinh_giay_phep_truoc = fields.Image(string="Ảnh giấy phép (Mặt trước)")
    hinh_giay_phep_sau = fields.Image(string="Ảnh giấy phép (Mặt sau)")