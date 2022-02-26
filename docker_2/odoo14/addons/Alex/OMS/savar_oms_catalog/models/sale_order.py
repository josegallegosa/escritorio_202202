
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = 'sale.order'

    merchant_account = fields.Many2one('res.partner', string="Comerciante", domain="[('merchant_catalog_owner', '=', True)]")
    
    def get_merchant_orders_count(self):
        partner = request.env.user.partner_id
        domain = [ 
                    ['merchant_account', '=', int(partner.id)]
                 ]
        orders = request.env['sale.order'].sudo().search(domain)
        _logger.warning("orders get_merchant_orders_count")
        _logger.warning(orders)
        _logger.warning(domain)
        count = int(0)
        if(orders):
            count = len(orders)
        else:
            count = 0
        return count