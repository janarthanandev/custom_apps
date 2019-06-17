# -*- coding: utf-8 -*-
from odoo import http

# class NewsFeed(http.Controller):
#     @http.route('/news_feed/news_feed/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/news_feed/news_feed/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('news_feed.listing', {
#             'root': '/news_feed/news_feed',
#             'objects': http.request.env['news_feed.news_feed'].search([]),
#         })

#     @http.route('/news_feed/news_feed/objects/<model("news_feed.news_feed"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('news_feed.object', {
#             'object': obj
#         })