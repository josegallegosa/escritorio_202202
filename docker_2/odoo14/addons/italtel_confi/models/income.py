# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Income(models.Model):
	_name = 'income'
	_description = 'Income'
	_rec_name = 'income_type'

	income_type = fields.Many2one(comodel_name='income.type', string='Income Type')
	year = fields.Integer(string='Year')
	exchange_rate = fields.Float(string='Exchange Rate')
	amount_sol = fields.Float(string='Amount Sol')
	amount_thousands_usd = fields.Float(string='Amount Thousands USD')