from odoo import api, fields, models, _

class Production(models.Model):
    _inherit = 'mrp.production'

    history_control = fields.One2many(
        comodel_name='history.qty.control',
        inverse_name='production_id',
        string='History Control',
        required=False, copy=False)
    use_history_control = fields.Boolean(
        string='Use history control',
        required=False, compute='_compute_use_history_control')

    @api.depends('bom_id')
    def _compute_use_history_control(self):
        for rec in self:
            rec.use_history_control = True
            if rec.bom_id.no_history_control:
                rec.use_history_control = False



    def create_history(self):
        lines = self._prepare_history_lines()

        wizard = self.env['production.history.wizard'].create({
            'production_id': self.id,
            'line_ids': lines
        })

        return {
            'name': _('Production Control'),
            'type': 'ir.actions.act_window',
            'res_model': 'production.history.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new'
        }

    def _get_product_to_history(self):
        excluded_products = self.bom_id.byproduct_ids.filtered(lambda r: r.no_history_control).ids

        byproducts = []
        if excluded_products:
            if len(excluded_products) > 1:
                byproducts = self.move_byproducts_ids.filtered(lambda r: r.id not in excluded_products.ids)
            else:
                byproducts = self.move_byproducts_ids.filtered(lambda r: not r.id == excluded_products.id)
        else:
            byproducts = self.move_byproducts_ids

        return byproducts


    def _prepare_history_lines(self):
        now = fields.Datetime.now()
        products = self._get_product_to_history()

        line_history = []

        for product in products:
            line_history.append((0, 0,
                {
                    'product_id': product.product_id.id,
                    'uom_id': product.product_uom.id,
                    'date': now,
                    'qty_producing': product.product_uom_qty,
                    'stock_move_id': product.id
                }
            ))

        line_history.append((0, 0,
                {
                    'product_id': self.product_id.id,
                    'uom_id': self.product_uom_id.id,
                    'date': now,
                    'qty_producing': self.qty_producing,
                    'is_main_product': True
                }
            ))

        return line_history




