# -*- coding: utf-8 -*-

from odoo import models, fields

class news_feed(models.Model):
    _name = 'news.feed'

    name = fields.Char()
    quotes = fields.Binary()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100