# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Project(models.Model):
	_inherit = 'project.task'
	
	estimated_time = fields.Float(string="Tiempo estimado")
	date_start = fields.Date(default=fields.Date.context_today, string='Fecha Inicio')

