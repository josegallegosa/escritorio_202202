
# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar

    
class FixedConceptsContract(models.Model):
    _name = "fixed.concepts.contract" 

    amount = fields.Float("Monto")
    input_type_id = fields.Many2one(comodel_name='hr.payslip.input.type',string='Tipo de entrada')
    contract_id = fields.Many2one(comodel_name='hr.contract',string='Contrato')

class HRContractInherit(models.Model):
    _inherit = "hr.contract" 
    
    fixed_concepts_ids = fields.One2many(comodel_name='fixed.concepts.contract',inverse_name='contract_id',string='Conceptos Fijos')
    



    
