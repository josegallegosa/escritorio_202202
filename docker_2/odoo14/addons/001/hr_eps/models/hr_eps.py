# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError


class HREnsuranceCompany(models.Model):
	_name = 'hr.ensure.company'
	_description = 'Compañía de Seguros'

	name = fields.Char(string='Compañía de Seguros')
	

class HREnsurancePlan(models.Model):
	_name = 'hr.ensure.plan'
	_description = 'Plan de Seguro'

	name = fields.Char(string='Plan')
	ensure_company_id = fields.Many2one(comodel_name='hr.ensure.company',string='Compañía de Seguros')
	

class HREmployeeEPS(models.Model):
	_name = 'hr.employee.eps'
	_description = 'Tabla EPS'
	_rec_name = 'employee_id'

	employee_id = fields.Many2one(comodel_name='hr.employee',string='Empleado')
	ensure_company_id = fields.Many2one(comodel_name='hr.ensure.company',string='Compañía de Seguros')
	ensure_plan_id = fields.Many2one(comodel_name='hr.ensure.plan',string='Plan')
	amount = fields.Float(string='Monto')
	amount_assumed_company = fields.Float(string='Monto asumido por empresa')

	def get_amount_eps(self,employee_id):
		eps_id = self.search([('employee_id','=',employee_id.id)],limit=1)
		vals={}
		if not eps_id:
			vals['amount']=0
			vals['amount_assumed_company']=0
		else:
			vals['amount']=eps_id.amount
			vals['amount_assumed_company']=eps_id.amount_assumed_company
		return vals


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def _compute_rule(self, localdict):
        self.ensure_one()
        localdict['eps_obj'] = self.env['hr.employee.eps']
        return super(HrSalaryRule,self)._compute_rule(localdict)

    def _satisfy_condition(self, localdict):
        self.ensure_one()
        localdict['eps_obj'] = self.env['hr.employee.eps']
        return super(HrSalaryRule, self)._satisfy_condition(localdict)