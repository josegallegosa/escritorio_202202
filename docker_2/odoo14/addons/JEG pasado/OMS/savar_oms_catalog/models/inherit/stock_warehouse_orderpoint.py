
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class StockWarehouseOrderpoint(models.Model):
    _inherit = 'stock.warehouse.orderpoint'
