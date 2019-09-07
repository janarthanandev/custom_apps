from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    exchange_id = fields.Many2one('stock.exchange', string='Exchange Reference', copy=False)