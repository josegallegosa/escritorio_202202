# -*- coding: utf-8 -*-
import logging

from odoo import fields, models, api
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

def year_now():
    return datetime.now().year

YEAR_SELECTION = [(str(year), year) for year in range(1450, year_now()+2)]


class ResPartner(models.Model):
    _inherit = 'res.partner'
    subscription_id = fields.Many2one(comodel_name='book.subscription', string='Proveedor')



class book_subscription(models.Model):
    _name = 'book.subscription'
    _description = 'Subscripción de la librería'

    supplier_id = fields.Many2one(comodel_name='res.partner', string='Proveedor')
    partner_ids =  fields.One2many('res.partner','subscription_id',string='Socio')
    parameter_shop = fields.Float('Precio Límite')

