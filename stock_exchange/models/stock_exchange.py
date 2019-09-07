# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from mock.mock import self

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
        ], string='Status', copy=False,  track_visibility='onchange', track_sequence=3, default='draft')
    
    @api.multi
    def create_exchange(self):
        print(self.exchange_line_ids)
        order_id = self.order_id
        order_line_obj = self.env['sale.order.line']
        for exchange_line in self.exchange_line_ids:
            order_line_obj.create({
                'product_id': exchange_line.exchange_product_id.id,
                'name': exchange_line.exchange_product_id.name,
                'order_id': order_id.id,
                'product_uom' : exchange_line.exchange_product_id.uom_id.id
                                })
            order_line_obj.product_id_change()
        self.write({'state':'done'})
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
#     
    @api.onchange('exchange_product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.exchange_product_id:
                line.price_unit = line.exchange_product_id.lst_price
            else:
                line.price_unit = 0.0
