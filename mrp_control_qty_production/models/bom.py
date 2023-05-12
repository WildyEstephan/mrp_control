from odoo import api, fields, models, _

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    no_history_control = fields.Boolean(
        string='No history control',
        required=False)

class MrpByProduct(models.Model):
    _inherit = 'mrp.bom.byproduct'

    no_history_control = fields.Boolean(
        string='No history control',
        required=False)

