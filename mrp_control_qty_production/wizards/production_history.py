from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductionHistory(models.TransientModel):
    _name = 'production.history.wizard'
    _description = 'Production History Wizard'

    production_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Production',
        required=False)
    line_ids = fields.One2many(
        comodel_name='production.history.ready.wizard',
        inverse_name='history_id',
        string='Line',
        required=False)

    def create_control_history(self):

        for line in self.line_ids:

            for employee in line.employee_ids:
                self.env['history.qty.control'].create({
                    'production_id': self.production_id.id,
                    'product_id': line.product_id.id,
                    'employee_id': employee.id,
                    'date': fields.Datetime.now(),
                    'product_uom_qty': line.product_uom_qty,
                    'is_main_product': line.is_main_product,
                    'uom_id': line.uom_id.id
                })

    def produce(self):

        if self.line_ids.filtered(lambda r: r.product_uom_qty <= 0):
            raise ValidationError(_("The quantities must be greater than 0."))

        if self.line_ids.filtered(lambda r: not r.employee_ids):
            raise ValidationError(_("You must has employee in all lines."))

        self.create_control_history()

        byproducts = self.line_ids.filtered(lambda r: not r.is_main_product)

        for byproduct in byproducts:
            if byproduct.stock_move_id.move_line_ids:
                byproduct.stock_move_id.move_line_ids[0].qty_done += byproduct.product_uom_qty
            else:
                move_line = byproduct.stock_move_id.move_line_ids.create({
                    'product_id': byproduct.stock_move_id.product_id.id,
                    'production_id': self.production_id.id,
                    'move_id': byproduct.stock_move_id.id,
                    'location_id': byproduct.stock_move_id.location_id.id,
                    'location_dest_id': byproduct.stock_move_id.location_dest_id.id,
                    'company_id': byproduct.stock_move_id.company_id.id,
                    'qty_done': byproduct.product_uom_qty,
                    'product_uom_id': byproduct.stock_move_id.product_uom.id
                })

        if self.line_ids.filtered(lambda r: r.is_main_product):
            main_product = self.line_ids.filtered(lambda r: r.is_main_product)[0]

            self.production_id.qty_producing += main_product.product_uom_qty


class ProductionHistoryReady(models.TransientModel):
    _name = 'production.history.ready.wizard'
    _description = 'Production History Ready Wizard'
    _order = 'is_main_product desc'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Uom',
        required=False)
    date = fields.Datetime(
        string='Date',
        required=False)
    employee_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Employee', domain="[('is_manufacturer', '=', True)]")
    qty_producing = fields.Float(
        string='Producing',
        required=False)
    product_uom_qty = fields.Float(
        string='Produced',
        required=False)
    is_main_product = fields.Boolean(
        string='Is main product',
        required=False)
    stock_move_id = fields.Many2one(
        comodel_name='stock.move',
        string='Stock Move',
        required=False)
    history_id = fields.Many2one(
        comodel_name='production.history.wizard',
        string='History',
        required=False)

