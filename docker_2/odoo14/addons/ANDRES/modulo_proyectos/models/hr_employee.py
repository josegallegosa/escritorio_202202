# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Hr(models.Model):
    _inherit = 'hr.employee'

    fecha_inicio_contrato = fields.Date(string='Fecha Inicio Contrato')
    #active = fields.Boolean(string='Activo?')





