
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class MrpPoduction(models.Model):
    _inherit = 'mrp.production'
