from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ThongKe(models.Model):
    _name = "thong_ke"
    _description = "Báo cáo thống kê phương tiện"

    total_vehicles_int = fields.Integer(string="Tổng số phương tiện (số)", compute="_compute_statistics", store=True)
    active_vehicles_int = fields.Integer(string="Xe đang hoạt động (số)", compute="_compute_statistics", store=True)
    maintenance_vehicles_int = fields.Integer(string="Xe bảo trì (số)", compute="_compute_statistics", store=True)
    available_vehicles_int = fields.Integer(string="Xe chưa giao (số)", compute="_compute_statistics", store=True)

    vehicle_by_type = fields.Text(string="Số lượng xe theo loại", compute="_compute_statistics", store=False)
    vehicle_by_driver = fields.Text(string="Số lượng xe theo tài xế", compute="_compute_statistics", store=False)

    studio_color = fields.Char(string="Màu sắc", compute="_compute_color", store=False)

    @api.depends()
    def _compute_statistics(self):
        Vehicle = self.env['phuong_tien']
        for record in self:
            record.total_vehicles_int = Vehicle.search_count([])
            record.active_vehicles_int = Vehicle.search_count([('status', '=', 'xe_da_giao')])
            record.maintenance_vehicles_int = Vehicle.search_count([('status', '=', 'xe_bao_tri')])
            record.available_vehicles_int = Vehicle.search_count([('status', '=', 'xe_chua_giao')])

            # Thống kê xe theo loại
            vehicle_types = Vehicle.read_group([], ['loai_xe_id'], ['loai_xe_id'])
            record.vehicle_by_type = "\n".join(
                [f"{t['loai_xe_id'][1]}: {t['loai_xe_id_count']}" for t in vehicle_types if t['loai_xe_id']]
            )

            # Thống kê xe theo tài xế
            vehicle_drivers = Vehicle.read_group([], ['driver_id'], ['driver_id'])
            record.vehicle_by_driver = "\n".join(
                [f"{d['driver_id'][1]}: {d['driver_id_count']}" for d in vehicle_drivers if d['driver_id']]
            )

            _logger.info(f"Thống kê phương tiện: Tổng {record.total_vehicles_int}, "
                         f"Hoạt động {record.active_vehicles_int}, "
                         f"Bảo trì {record.maintenance_vehicles_int}, "
                         f"Chưa giao {record.available_vehicles_int}")

    @api.depends()
    def _compute_color(self):
        """ Định nghĩa màu theo loại phương tiện """
        color_map = {
            'Xe máy': 'blue',
            'Ô tô': 'green',
        }
        for record in self:
            if hasattr(record, 'vehicle_type'):
                record.studio_color = color_map.get(record.vehicle_type, 'black')  # Mặc định là đen
            else:
                record.studio_color = 'black'

    @api.model
    def default_get(self, fields):
        rec = self.search([], limit=1)
        return rec.read(fields)[0] if rec else super().default_get(fields)

    _sql_constraints = [
        ('unique_thong_ke', 'UNIQUE(id)', 'Chỉ có một bản ghi thống kê!')
    ]
    @api.model
    def create(self, vals):
            # Xóa tất cả bản ghi cũ trước khi thêm bản ghi mới
        self.search([]).unlink()
        return super(ThongKe, self).create(vals)