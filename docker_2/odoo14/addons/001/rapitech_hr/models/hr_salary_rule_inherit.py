from odoo import models, fields, api

class HrPayslipInherit(models.Model):
    _inherit = 'hr.salary.rule'

    is_distributes_debit_account = fields.Boolean(string="Distribuye Cuenta Deudora", default=True)
    is_distributes_creditor_account = fields.Boolean(string="Distribuye Cuenta Acreedora", default=True)