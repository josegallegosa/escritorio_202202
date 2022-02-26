# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    payment_mode = fields.Selection(
    	string="Modo de pago",
    	selection=[
    		('cash', 'Cash'),
    		('bank', 'Bank'),
    		('electronic', 'Electronic'),
    	], default="electronic"
    )	
    
