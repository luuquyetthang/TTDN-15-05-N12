import json
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

    @api.depends()
    def _compute_statistics(self):
        Vehicle = self.env['phuong_tien']
        for record in self:
            record.total_vehicles_int = Vehicle.search_count([])
            record.active_vehicles_int = Vehicle.search_count([('status', '=', 'xe_da_giao')])
            record.maintenance_vehicles_int = Vehicle.search_count([('status', '=', 'xe_bao_tri')])
            record.available_vehicles_int = Vehicle.search_count([('status', '=', 'xe_chua_giao')])

            vehicle_types = Vehicle.read_group([], ['loai_xe_id'], ['loai_xe_id'])
            vehicle_data = {
                "labels": [self.env['loai_xe'].browse(t['loai_xe_id'][0]).name for t in vehicle_types if t['loai_xe_id']],
                "values": [t['loai_xe_id_count'] for t in vehicle_types if t['loai_xe_id']]
            }
            record.vehicle_by_type = json.dumps(vehicle_data, ensure_ascii=False)

            vehicle_drivers = Vehicle.read_group([], ['driver_id'], ['driver_id'])
            driver_data = {
                "labels": [self.env['res.partner'].browse(t['driver_id'][0]).name for t in vehicle_drivers if t['driver_id']],
                "values": [t['driver_id_count'] for t in vehicle_drivers if t['driver_id']]
            }
            record.vehicle_by_driver = json.dumps(driver_data, ensure_ascii=False)

            _logger.info(f"Thống kê phương tiện: Tổng {record.total_vehicles_int}, "
                         f"Hoạt động {record.active_vehicles_int}, "
                         f"Bảo trì {record.maintenance_vehicles_int}, "
                         f"Chưa giao {record.available_vehicles_int}")

    @api.model
    def default_get(self, fields):
        rec = self.search([], limit=1)
        return rec.read(fields)[0] if rec else super().default_get(fields)

    _sql_constraints = [
        ('unique_thong_ke', 'UNIQUE(id)', 'Chỉ có một bản ghi thống kê!')
    ]

    @api.model
    def create(self, vals):
        self.search([]).unlink()
        return super(ThongKe, self).create(vals) 