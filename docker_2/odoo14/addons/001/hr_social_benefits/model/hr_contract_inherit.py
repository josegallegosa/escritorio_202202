
# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar

class HRInheritContract(models.Model):
    _inherit = "hr.contract" 

    last_salary_change_date = fields.Date(string='Fecha último cambio de sueldo')
    is_change_salary = fields.Boolean(string="Es cambio de salario?", default=False)

    @api.onchange('wage')
    def _onchange_wage(self):
        print("Entró _onchange_wage")
        self.is_change_salary = True
    
    def write(self, vals):
        res = super(HRInheritContract, self).write(vals)

        employees = self.env['hr.employee'].search([('company_id', '=', self.env.company.id)])
        contracts = self.env['hr.contract'].search([('state', '=', 'open')])
        list_contract = []
        for contract in contracts:
            list_contract.append(contract.id)
        employee_ids = self.env['hr.employee'].search([('contract_id','in',list_contract)])
        #employee = self.env
        #contracts_ids = employee._get_contracts(datetime.datetime(current_date.year-1, 12, 1))
        for employee in employee_ids:
         print(employee.name)

        #print("is_change_salary ", self.is_change_salary)
        return res
    