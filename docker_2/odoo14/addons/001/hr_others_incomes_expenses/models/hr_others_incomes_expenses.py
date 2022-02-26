# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class HrPayslipInputType(models.Model):
    _inherit = 'hr.payslip.input.type'

    afecta_todo = fields.Boolean(string='Afecta toda la compañia')
    percent_of_base = fields.Float(string='Porcentaje de la base remunerativa')


class HROthersIncomesExpenses(models.Model):
    _name = 'hr.others.incomes.expenses'
    _description='Otros ingresos o egresos'

    name = fields.Char(string='Nombre', required=True)
    line_ids = fields.One2many(comodel_name='hr.others.incomes.expenses.line',
                               inverse_name='other_income_expense_id', readonly=True,
                               states={'draft': [('readonly', False)]},
                               string='Líneas de ingreso o egreso')
    date = fields.Date(string='Fecha', readonly=True,
                                states={'draft': [('readonly', False)]})
    state = fields.Selection(selection=[('draft', 'Borrador'), ('validate', 'Validado')],
                             string='Estado', default='draft')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    input_type_id = fields.Many2one(comodel_name='hr.payslip.input.type', string='Tipo de input', required=True)

    
    def action_validate(self):
        for income_expense in self:
            income_expense.state = 'validate'

    @api.model
    def create_details(self, income_expense):
        if income_expense.input_type_id.afecta_todo:
            employee_ids = self.env['hr.employee'].search([('company_id', '=', income_expense.company_id.id)])
            for employee in employee_ids:
                contract = self.env['hr.contract'].search([('employee_id', '=', employee.id)], order='date_start desc', limit=1)
                val = {
                'employee_id': employee.id,
                'amount': contract.wage*income_expense.input_type_id.percent_of_base/100,
                'other_income_expense_id': income_expense.id}
                self.env['hr.others.incomes.expenses.line'].create(val)

    @api.model
    def create(self, vals):
        my_id = super(HROthersIncomesExpenses, self).create(vals)
        self.create_details(my_id)
        return my_id


class HROthersIncomesExpensesLine(models.Model):
    _name = 'hr.others.incomes.expenses.line'
    _description = 'Líneas de otros ingresos o egresos'

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado')
    amount = fields.Float(string='Monto')
    other_income_expense_id = fields.Many2one(comodel_name='hr.others.incomes.expenses', string='Otro ingreso o egreso')

    percent = fields.Float('Porcentaje')

    @api.onchange('percent')
    def onchange_percent(self):
        if self.percent:
            contract_id = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),
                ('state','=','open')], limit=1)
            self.amount = (self.percent/100)*contract_id.wage

    @api.onchange('amount')
    def onchange_amount(self):
        if self.amount:
            contract_id = self.env['hr.contract'].search([('employee_id','=',self.employee_id.id),
                ('state','=','open')], limit=1)
            self.percent = (self.amount/contract_id.wage)*100

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_id, date_from, date_to):
        self.ensure_one()
        incomes_expenses = self.env['hr.others.incomes.expenses'].search([('date', '>=', date_from), ('date', '<=', date_to), ('state', '=', 'validate')]).ids
        employee_incomes_expenses = self.env['hr.others.incomes.expenses.line'].search([('other_income_expense_id', 'in', incomes_expenses), ('employee_id', '=', contract_id.employee_id.id)])
        sequence=0
        res=[]
        for line in employee_incomes_expenses:
            print ('++++++++++++++++++++++++++++', line)
            sequence+=1
            input_data = {
                'input_type_id': line.other_income_expense_id.input_type_id.id,
                'sequence':sequence,
                'amount': line.amount,
                'contract_id': contract_id.id,
            }
            res.append(input_data)
        return res

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        res = super(HrPayslip,self)._onchange_employee()
        input_lines = self.input_line_ids.browse([])
        for input in self.get_inputs(self.contract_id,self.date_from,self.date_to):
            input_lines |= input_lines.new(input)
        self.input_line_ids = input_lines
        return res
