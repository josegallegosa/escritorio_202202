# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class savar_demo_data(models.Model):
#     _name = 'savar_demo_data.savar_demo_data'
#     _description = 'savar_demo_data.savar_demo_data'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
