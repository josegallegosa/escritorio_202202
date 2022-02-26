# -*- coding: utf-8 -*-
# from odoo import http


# class SavarDemoData(http.Controller):
#     @http.route('/savar_demo_data/savar_demo_data/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/savar_demo_data/savar_demo_data/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('savar_demo_data.listing', {
#             'root': '/savar_demo_data/savar_demo_data',
#             'objects': http.request.env['savar_demo_data.savar_demo_data'].search([]),
#         })

#     @http.route('/savar_demo_data/savar_demo_data/objects/<model("savar_demo_data.savar_demo_data"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('savar_demo_data.object', {
#             'object': obj
#         })
