# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class website_sale_order(http.Controller):

    @http.route(['/orders/create'], type='json', auth='public', methods=['POST'], website=True)
    def order_create(self, sequence, partner_id, partner_invoice_id, partner_delivery_id, lines):
        _logger.warning("#########################")
        _logger.warning(partner_id)
        _logger.warning(partner_invoice_id)
        _logger.warning(partner_delivery_id)
        _logger.warning(lines)

        values = {  
                    'name': str(sequence),
                    'partner_id': int(partner_id),
                    'partner_invoice_id': int(partner_invoice_id),
                    'partner_shipping_id': int(partner_delivery_id),

                 }
        _logger.warning(values)
        _logger.warning("#########################")
        order_id = request.env['sale.order'].sudo().create(values)
        if(lines):
            for _line in lines:
                _logger.warning('_line')
                _logger.warning(_line)
                _product = request.env['product.product'].sudo().search([
                                                                            ['product_tmpl_id', '=', int(_line['product_id'])]
                                                                        ], limit=1)
                new_line = request.env['sale.order.line'].sudo().create({
                                                                            'product_id': int(_product.id),
                                                                            'name': str(_line['product_description']),
                                                                            'order_id':order_id.id,                                                                            
                                                                            'product_uom_qty': str(_line['product_quantity']),
                                                                            'product_uom' : int(_product.uom_id.id),
                                                                            'price_unit' : float(_line['product_price'])
                                                                        })
                taxes =  _line['product_taxes']
                if(taxes):
                    _taxes_values = []
                    _taxes_ids = str(taxes).split(",")
                    if(_taxes_ids):
                        for _tax in _taxes_ids:
                            _taxes_values.append(int(_tax))
                        _logger.warning('_taxes_values')
                        _logger.warning(_taxes_values)
                        new_line.sudo().update({'tax_id': [[6, 0,_taxes_values]] })

                product_subservice =  _line['product_subservice']
                if(product_subservice):
                    new_line.sudo().update({'subservice_id': product_subservice })
                            
        return request.env['sale.order'].sudo().browse(int(order_id.id)).read()
