# -*- coding: utf-8 -*-
# from odoo import http


# class SavarOmsCatalog(http.Controller):
#     @http.route('/savar_oms_catalog/savar_oms_catalog/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/savar_oms_catalog/savar_oms_catalog/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('savar_oms_catalog.listing', {
#             'root': '/savar_oms_catalog/savar_oms_catalog',
#             'objects': http.request.env['savar_oms_catalog.savar_oms_catalog'].search([]),
#         })

#     @http.route('/savar_oms_catalog/savar_oms_catalog/objects/<model("savar_oms_catalog.savar_oms_catalog"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('savar_oms_catalog.object', {
#             'object': obj
#         })
