
# -- coding: utf-8 --
import base64
from odoo import api, models, fields
from odoo.exceptions import UserError
from datetime import datetime


class HRResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    _rec_name = 'bank_code' 

    bank_code = fields.Char(compute='_method_computado',string='Cuenta de Banco Compañia') 

    @api.depends('bank_id', 'acc_number')
    def _method_computado(self):
        for line in self:
            if line.bank_id.name == False or line.acc_number == False:
                line.bank_code = line.acc_number
            else:
                line.bank_code =  line.bank_id.name+'-'+line.acc_number


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    check_digit = fields.Char(comodel_name='res.partner', string='Dígito de verificación') 
    arl_id = fields.Many2one(string='ARL', comodel_name='hr.arl')    
    

    



    

    
