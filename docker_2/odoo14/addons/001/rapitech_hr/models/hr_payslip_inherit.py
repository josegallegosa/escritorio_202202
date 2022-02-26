from odoo import models, fields, api

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip'

    journal_id = fields.Many2one(related="contract_id.journal_id")