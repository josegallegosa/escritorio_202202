# -*- coding: utf-8 -*-
from odoo import fields,models
import logging
_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = "product.template"

    product_service_subservices = fields.Many2many('fsm.order.service', string='Servicio')

    def get_sale_taxes(self):
        return self.env['account.tax'].sudo().get_account_taxes_for_sale()
    
    def get_taxes_assigned(self, fields, domain):
        product_template = self.env['product.template'].sudo().search(domain)
        taxes = []
        taxes_preselection = []
        if(product_template):
            _logger.warning("product_template get_taxes_assigned")
            _logger.warning(product_template)
            if(product_template.taxes_id):
                _logger.warning("product_template.taxes_id get_taxes_assigned")
                _logger.warning(product_template.taxes_id)
                for taxes_ids in product_template.taxes_id:
                    taxes_preselection.append(int(taxes_ids.id))
                    tax = {
                            'id': str(taxes_ids.id) ,
                            'text': str(taxes_ids.name) ,
                          }
                    taxes.append(tax)
                _logger.warning("taxes get_taxes_assigned")
                _logger.warning(taxes)
        return { 
                'taxes_preselection':taxes_preselection, 
                'taxes':taxes 
               }
    
    def save_values(self, params):
        
        _logger.warning('save_values params')
        _logger.warning(params)

        if('name' in params):
            self.env['product.template'].sudo().update({'name':params['name']})
        if('list_price' in params):
            self.env['product.template'].update({'list_price':params['list_price']})
        if('default_code' in params):
            self.env['product.template'].update({'default_code':params['default_code']})
        if('barcode' in params):
            self.env['product.template'].update({'barcode':params['barcode']})
        if('public_description' in params):
            self.env['product.template'].update({'public_description':params['public_description']})
        
        # if('product_service' in params):
        #     self.env['product.template'].update({'product_service':int(params['product_service'])})
        # if('product_subservice' in params):
        #     self.env['product.template'].update({'product_subservice':int(params['product_subservice'])})
        
        if('taxes_id' in params):
            taxes = []
            if(params['taxes_id']):
                for tax in params['taxes_id']:
                    taxes.append(tax)

            self.env['product.template'].update({'taxes_id':[6,0,taxes]})
        
