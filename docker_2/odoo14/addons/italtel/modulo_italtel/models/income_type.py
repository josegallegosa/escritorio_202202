# -*- coding: utf-8 -*-
from odoo import models, fields, api

class IncomeType(models.Model):
	_name = 'income.type'
	_description = 'Income Type'

	name = fields.Char(string='Income Type')
	description = fields.Char(string='Description')