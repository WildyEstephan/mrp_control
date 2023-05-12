from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    use_history_controll = fields.Boolean(
        string='Use history control',
        required=False, related='production_id.use_history_control')
