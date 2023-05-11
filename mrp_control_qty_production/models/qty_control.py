from odoo import api, fields, models, _


class HistoryQTYControl(models.Model):
    _name = 'history.qty.control'
    _description = 'History QTY Control'

    production_id = fields.Many2one(
        comodel_name='mrp.production',
        string='Production',
        required=False)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Uom',
        required=False)
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        required=False)
    date = fields.Datetime(
        string='Date', 
        required=False)
    product_uom_qty = fields.Float(
        string='Produce',
        required=False)
    is_main_product = fields.Boolean(
        string='Is main product',
        required=False)
