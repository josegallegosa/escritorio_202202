# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResUsers(models.Model):
	_inherit = 'res.users'
	
	share = fields.Boolean(compute='', compute_sudo=False, string='Share User', store=True,
         help="External user with limited access, created only for the purpose of sharing data.",default=False,readonly=False)

