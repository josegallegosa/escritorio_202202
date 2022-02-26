# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from datetime import datetime
import math



class Hr5taParameterLine(models.Model):
    _name = 'hr.retencion.line'
    _description = 'Escalas de Retención en la Fuente'
    _rec_name = 'sequence'
    _order = 'sequence'

    sequence = fields.Integer(string='Secuencia')
    init_value = fields.Integer(string='Valor inicial')
    final_value = fields.Integer(string='Valor final')
    marginal_rate = fields.Float(string='Tarifa Marginal')
    additional_value = fields.Float(string='Valor Adicional')

    def get_scales_retencion(self):
        scales = self.env['hr.retencion.line'].search([],order='sequence')
        list_scales=[]
        
        for scale in scales:
            dict_scale={}
            dict_scale['lower_limit'] = scale.init_value
            dict_scale['upper_limit'] = scale.final_value if scale.final_value>0 else math.inf
            dict_scale['percentage'] = scale.marginal_rate
            dict_scale['additional'] = scale.additional_value
            list_scales.append(dict_scale)
        return list_scales

