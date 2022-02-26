# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    def action_open_payslips(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.payslip",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['id', 'in', self.slip_ids.ids]],
            "context": {'default_payslip_run_id': self.id},
            "name": "Payslips",
        }

class HrPayslipStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    is_load_auto_lot = fields.Boolean('Carga Automática en Lotes') 
    