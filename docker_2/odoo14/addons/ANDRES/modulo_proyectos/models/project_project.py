# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProjectProject(models.Model):
	_inherit = 'project.project'
	
	department_id = fields.Many2one('hr.department',string="Área o Departamento")
	# ya existe # date_start = fields.Date(string="Fecha Inicio")
	date_end = fields.Date(string="Fecha Fin")

	#partner_id = fields.Many2one('res.partner', string='Customer', auto_join=True, tracking=True, domain="[('is_company', '=', True)]")

	#allowed_internal_user_ids = fields.Many2many('res.users', 'project_allowed_internal_users_rel',
    #                                            string="Allowed Internal Users", default=lambda self: self.env.user, domain=[])