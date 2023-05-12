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

    def action_view_history_production(self):
        action = self.env['ir.actions.act_window']._for_xml_id('mrp_control_qty_production.history_qty_control_action')
        action["domain"] = [("employee_id", "=", self.id)]
        return action

