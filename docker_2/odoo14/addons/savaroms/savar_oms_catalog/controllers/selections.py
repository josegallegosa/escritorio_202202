# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class selections(http.Controller):

    @http.route(['/selections/taxes/search_read'], type='json', auth='public', methods=['POST'], website=True)
    def slide_channel_tag_search_read(self, fields, domain):
        can_create = request.env['account.tax'].check_access_rights('create', raise_exception=False)
        return {
                    'read_results': request.env['account.tax'].search_read(domain, fields),
                    'can_create': can_create,
                }
    
    @http.route(['/selections/taxes/get_taxes_assigned'], type='json', auth='public', methods=['POST'], website=True)
    def get_taxes_assigned(self, fields, domain):
        taxes = request.env['product.template'].sudo().get_taxes_assigned(fields, domain)
        return taxes
    
    @http.route(['/selections/partner/get_partners'], type='json', auth='public', methods=['POST'], website=True)
    def get_partners(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)
        return {
                    'read_results': request.env['res.partner'].search_read(domain, fields),
                    'can_create': can_create,
                }
    
    @http.route(['/selections/partner/get_invoice_partner_childs'], type='json', auth='public', methods=['POST'], website=True)
    def get_invoice_partner_childs(self, fields, domain):
        can_create = request.env['res.partner'].check_access_rights('create', raise_exception=False)
        _logger.warning('#######################')
        _logger.warning(domain)
        _logger.warning(fields)
        _logger.warning(request.env['res.partner'].search_read(domain, fields))
        _logger.warning('***********************')
        return {
                    'read_results': request.env['res.partner'].search_read(domain, fields),
                    'can_create': can_create,
                }
        
    @http.route(['/selections/products/get_products'], type='json', auth='public', methods=['POST'], website=True)
    def get_products(self, fields, domain):
        can_create = request.env['product.template'].check_access_rights('create', raise_exception=False)
        _logger.warning('#######################')
        _logger.warning(domain)
        _logger.warning(fields)
        _logger.warning(request.env['product.template'].search_read(domain, fields))
        _logger.warning('***********************')
        return {
                    'read_results': request.env['product.template'].search_read(domain, fields),
                    'can_create': can_create,
                }
    
    @http.route(['/selections/products/get_services'], type='json', auth='public', methods=['POST'], website=True)
    def get_services(self, fields, domain):
        _logger.warning('#######################')
        _logger.warning(domain)
        _logger.warning(fields)
        _logger.warning(request.env['fsm.order.service'].search_read(domain, fields))
        _logger.warning('***********************')
        can_create = request.env['fsm.order.service'].check_access_rights('create', raise_exception=False)
        read_results = request.env['fsm.order.service'].search_read(domain, fields)
        if(read_results):
            index = 0
            for result in read_results:
                current_name = str(read_results[index]['name'])

                service = request.env['fsm.order.service'].browse(int(result['id']))
                parent_name = str("")
                if(service):
                    parent_name = str(service.parent_id.name) + str(' - ')                
                
                read_results[index]['name'] = str(parent_name) + str(current_name) 
                index += int(1)
                
                _logger.warning(result)
        return  {
                    'read_results': read_results,
                    'can_create': can_create,
                }