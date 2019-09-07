# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class stock_exchange(models.Model):
    _name = 'stock.exchange'
 
    name = fields.Char()
    partner_id = fields.Many2one('res.partner', string='Customer', help="For whom the product is going to be exchanged")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    order_line_ids = fields.One2many('sale.order.line', 'exchange_id',string='Ordered Products')
    exchange_line_ids = fields.One2many('stock.exchange.line', 'exchange_id',string='Exchange New Product')
    
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', track_sequence=3, default='draft')
    
#     @api.onchange('order_line_ids','order_line.product_id')
#     def _onchange_product_id(self):
#         for line in self.order_line_ids:
#             if line.product_id:
#                 line.price_unit = line.product_id.lst_price
#             else:
#                 line.price_unit = 0.0
#     @api.multi
#     def write(self, vals):
#         res = super(stock_exchange, self).write(vals)
#         if 'order_line' in vals:
#             vals['order_line'].mapped('order_id') = self.order_id
#         return res
    
    @api.onchange('order_id')
    def onchange_order_id(self):
        self.order_line_ids = self.order_id.order_line

    
    
class Stock_Exchange_Line(models.Model):
    _name = 'stock.exchange.line'
    
    exchange_id = fields.Many2one('stock.exchange', string='Exchange Reference', copy=False)
    exchange_product_id = fields.Many2one('product.product', "Exchange Product", domain=[('sale_ok', '=', True)])
    product_uom_qty = fields.Float(string='Ordered Quantity')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
#     price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
#     price_tax = fields.Float(compute='_compute_amount', string='Total Tax', readonly=True, store=True)
#     price_total = fields.Monetary(compute='_compute_amount', string='Total', readonly=True, store=True)
#     
    @api.onchange('exchange_product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.exchange_product_id:
                line.product_uom = line.exchange_product_id.product_uom
                line.price_unit = line.exchange_product_id.lst_price
            else:
                line.price_unit = 0.0
#     
#     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
#     def _compute_amount(self):
#          for line in self:
#             price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
#             taxes = line.tax_id.compute_all(price, line.exchange_id.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.exchange_id.order_id.partner_shipping_id)
#             line.update({
#                 'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
#                 'price_total': taxes['total_included'],
#                 'price_subtotal': taxes['total_excluded'],
#             })
#     