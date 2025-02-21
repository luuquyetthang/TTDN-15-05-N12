from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'  # Đặt tên hiển thị mặc định trong view tìm kiếm
    _order = 'ma_dinh_danh ASC'  # Sắp xếp mặc định theo mã định danh tăng dần
    
    # Các trường dữ liệu
    ma_dinh_danh = fields.Char("Mã định danh", required=True, index=True)
    ten_dem = fields.Char("Tên đệm")
    ten_dinh_danh = fields.Char("Tên định danh")
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    ngay_sinh = fields.Date("Ngày sinh")
    tuoi = fields.Integer("Tuổi", compute="_compute_tuoi", store=True)
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    
    # Quan hệ với bảng lịch sử công tác
    lich_su_cong_tac_ids = fields.One2many(
        comodel_name="lich_su_cong_tac",
        inverse_name="nhan_vien_id",
        string="Lịch sử công tác"
    )

    # Tính toán họ và tên
    @api.depends("ten_dem", "ten_dinh_danh")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ten_dem and record.ten_dinh_danh:
                record.ho_va_ten = f"{record.ten_dem} {record.ten_dinh_danh}"
            else:
                record.ho_va_ten = record.ten_dinh_danh or record.ten_dem or ""

    # Tính toán tuổi từ ngày sinh
    @api.depends("ngay_sinh")
    def _compute_tuoi(self):
        today = fields.Date.today()
        for record in self:
            if record.ngay_sinh:
                record.tuoi = today.year - record.ngay_sinh.year - (
                    (today.month, today.day) < (record.ngay_sinh.month, record.ngay_sinh.day)
                )
            else:
                record.tuoi = 0

    # Tự động tạo mã định danh từ tên đệm và tên định danh
    @api.onchange("ten_dem", "ten_dinh_danh")
    def _onchange_ma_dinh_danh(self):
        for record in self:
            if record.ten_dem and record.ten_dinh_danh:
                chu_cai_dau = ''.join([tu[0] for tu in record.ten_dem.lower().split()])
                record.ma_dinh_danh = f"{record.ten_dinh_danh.lower()}{chu_cai_dau}"

    # Ràng buộc tuổi không được nhỏ hơn 18
    @api.constrains("tuoi")
    def _check_tuoi(self):
        for record in self:
            if record.tuoi < 18:
                raise ValidationError("Tuổi không được nhỏ hơn 18!")

    # Ràng buộc mã định danh phải là duy nhất
    _sql_constraints = [
        ('unique_ma_dinh_danh', 'UNIQUE(ma_dinh_danh)', 'Mã định danh phải là duy nhất!')
    ]

    # Hàm tìm kiếm nhân viên theo mã định danh, họ tên hoặc quê quán
    def tim_kiem_nhan_vien(self, keyword):
        domain = ['|', '|',
                  ('ma_dinh_danh', 'ilike', keyword),
                  ('ho_va_ten', 'ilike', keyword),
                  ('que_quan', 'ilike', keyword)]
        return self.search(domain, limit=10, offset=0, order=None, count=False)

