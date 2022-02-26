# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models


class HRPayrollParametersLine(models.Model):
    _name = 'hr.payroll.parameters.line'
    _description='Líneas de parámetros de nómina'

    date_start = fields.Date(string='Fecha de Inicio')
    parameter_id = fields.Many2one(comodel_name='hr.payroll.parameters',
                                   string='Parámetro',
                                   required=True)
    amount = fields.Float(string='Monto',
                          help="Monto en soles", required=True)

    company_id = fields.Many2one('res.company','Compañia',related="parameter_id.company_id")
    
    def get_amount(self, code,  date):
        parameter = self.env['hr.payroll.parameters'].search([('code', '=', code)],limit=1)
        val = self.search(['&', ('date_start', '<=', date), ('parameter_id', '=', parameter.id)],order='date_start')
        return val[-1].amount


class HRPayrollParameters(models.Model):
    _name = 'hr.payroll.parameters'
    _description = 'Parámetros de nómina'

    name = fields.Char(string='Nombre')
    code = fields.Char(string='Código')
    line_ids = fields.One2many(comodel_name='hr.payroll.parameters.line',
                               inverse_name='parameter_id',
                               string='Líneas')
    country_id = fields.Many2one('res.country','País',default=lambda self:self.env.user.company.country_id.id)
    company_id = fields.Many2one('res.company','Compañia',default=lambda self:self.env.company.id)

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def _compute_rule(self, localdict):
        self.ensure_one()
        localdict['parameter_obj'] = self.env['hr.payroll.parameters.line']
        return super(HrSalaryRule,self)._compute_rule(localdict)

    def _satisfy_condition(self, localdict):
        self.ensure_one()
        localdict['parameter_obj'] = self.env['hr.payroll.parameters.line']
        return super(HrSalaryRule, self)._satisfy_condition(localdict)
