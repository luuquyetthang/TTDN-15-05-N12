from odoo import models,fields,api
class PhuongTien(models.Model):
    _name = "phuong_tien"
    _description = "Danh mục phương tiện"

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    maintenance_date = fields.Date(string="Maintenance Date", required=True)
    description = fields.Text(string="Description")
    cost = fields.Float(string="Cost")
    next_maintenance_date = fields.Date(string="Next Maintenance Date")

    @api.onchange('maintenance_date')
    def _compute_next_maintenance(self):
        if self.maintenance_date:
            self.next_maintenance_date = fields.Date.add(self.maintenance_date, months=6)