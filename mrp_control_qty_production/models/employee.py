from odoo import api, fields, models, _

class Employee(models.Model):
    _inherit = 'hr.employee'

    is_manufacturer = fields.Boolean(
        string='Is manufacturer',
        required=False)
    history_production_ids = fields.One2many(
        comodel_name='history.qty.control',
        inverse_name='employee_id',
        string='History Production',
        required=False)

