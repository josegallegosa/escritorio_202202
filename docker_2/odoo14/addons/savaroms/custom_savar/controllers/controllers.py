# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSavar(http.Controller):
#     @http.route('/custom_savar/custom_savar/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_savar/custom_savar/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_savar.listing', {
#             'root': '/custom_savar/custom_savar',
#             'objects': http.request.env['custom_savar.custom_savar'].search([]),
#         })

#     @http.route('/custom_savar/custom_savar/objects/<model("custom_savar.custom_savar"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_savar.object', {
#             'object': obj
#         })
