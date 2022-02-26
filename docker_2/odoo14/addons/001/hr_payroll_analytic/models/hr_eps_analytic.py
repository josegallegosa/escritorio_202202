# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError


class HRPayrollAnalyticEmployee(models.Model):
	_name = 'hr.payroll.analytic.employee'
	_description = 'Distribución de costos'

	contract_id = fields.Many2one(comodel_name='hr.contract',string="Contrato")
	percent = fields.Float(string='Porcentaje')
	analytic_account_id = fields.Many2one(comodel_name='account.analytic.account',string="Cuenta Analítica")



class HREmployee(models.Model):
	_inherit = 'hr.contract'
		
	payroll_analytic_ids =  fields.One2many('hr.payroll.analytic.employee','contract_id','Costos')


