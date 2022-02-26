# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class website_sale_order(http.Controller):

    @http.route(['/orders/create'], type='json', auth='public', methods=['POST'], website=True)
    def order_create(self, order_id, sequence, partner_id, partner_invoice_id, partner_delivery_id, lines):
        partner = request.env.user.partner_id
        values = {  
                    'name': str(sequence),
                    'partner_id': int(partner_id),
                    'merchant_account': int(partner.id),
                    'partner_invoice_id': int(partner_invoice_id),
                    'partner_shipping_id': int(partner_delivery_id),

                 }
        
        _logger.warning("website_sale_order #########################")
        _logger.warning(values)
        _logger.warning(order_id)

        if(int(order_id) > 0): # edit mode
            order_id = request.env['sale.order'].sudo().browse(int(order_id))
        else: # new one mode
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

    @http.route(['/orders/get_values'], type='json', auth='public', methods=['POST'], website=True)
    def get_order_values(self, order_id):
        order = None
        response = []
        if(order_id):
            order = request.env['sale.order'].browse(int(order_id))
            order_lines = []
            if(order):
                response = {
                                'id': order.id,
                                'name': order.name,
                                'partner_invoice_id': order.partner_invoice_id.id,
                                'partner_invoice_name': order.partner_invoice_id.name,
                                'partner_delivery_id': order.partner_shipping_id.id,
                                'partner_delivery_name': order.partner_shipping_id.name,
                                'partner_id': order.partner_id.id,
                                'partner_id_name': order.partner_id.name,
                                'lines': [],
                            }
                if(order.order_line):
                    for line in order.order_line:
                        item =  {
                                    'id': line.id,
                                    'product_id': line.product_id.id,
                                    'product_id_name': line.product_id.name,
                                    'product_description': line.name,
                                    'quantity': line.product_uom_qty,
                                    'unit_price': line.price_unit,
                                    'taxes': self.get_order_values_taxes(line.tax_id),
                                    'subservice_id': line.subservice_id.id,
                                    'subservice_name': line.subservice_id.name,
                                }
                        order_lines.append(item)
                    response['lines'] = order_lines
        response['lines_count'] = len(response['lines'])
        return response                  
    
    def get_order_values_taxes(self, taxes):
        _taxes = []
        if(taxes):
            for tax in taxes:
                item = {'id':tax.id, 'text':tax.name}
                _taxes.append(item)
        return _taxes