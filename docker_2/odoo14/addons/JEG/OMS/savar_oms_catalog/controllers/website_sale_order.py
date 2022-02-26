# -*- coding: utf-8 -*-
from odoo import http
from odoo import models, fields, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)
import xlrd

class website_sale_order(http.Controller):

    def map_column(self, name):
        if(name == 'Referencia del pedido'):
            return 'sequence'
        elif(name == 'Cliente/Nombre'):
            return 'partner_id.name'
        elif(name == 'Cliente/NIF'):
            return 'partner_id.nif'
        else:
            return None

    @http.route(['/orders/massive_save'], type='http', auth='public', methods=['POST'], website=True)
    def orders_massive_save(self, **post):
        values = {}
        name = post.get('attachment').filename      
        file = post.get('attachment')
        excel_data = file.read()
        book = xlrd.open_workbook(file_contents=excel_data)
        _logger.warning("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        _logger.warning("EXCEL FILE")
        _logger.warning("-------------------")
        _logger.warning(name)
        # _logger.warning(book.sheets())
        worksheet = book.sheets()[0]
        first_row = []
        for col in range(worksheet.ncols):
            first_row.append( worksheet.cell_value(0,col) )
        data =[]
        for row in range(1, worksheet.nrows):
            elm = {}
            for col in range(worksheet.ncols):
                elm[first_row[col]]=worksheet.cell_value(row,col)
            data.append(elm)
            # save time: while collecting data will process
            if('Referencia del pedido' in elm):
                values['sequence'] = elm['Referencia del pedido']

            _domain = []
            if('Cliente/Nombre' in elm or 'Cliente/NIF' in elm):
                _domain = ['|']
                if(elm['Cliente/Nombre']):
                    _domain.append(elm['Cliente/Nombre'])
                if(elm['Cliente/NIF']):
                    _domain.append(elm['Cliente/NIF'])                                                
            elif('Cliente/Nombre' in elm and 'Cliente/NIF' in elm):
                _domain = [
                            ['name', '=', elm['Cliente/Nombre']],
                            ['vat', '=', elm['Cliente/NIF']]
                          ]             
            else:
                pass
        
        _logger.warning("_domain")
        _logger.warning(_domain)

        _logger.warning(data)

        _logger.warning("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        # sale_orders_massive = request.env['sale.orders.massive'].sudo().create({
        #                                                                             'name': str('Importación ') + str(fields.datetime.now()),
        #                                                                             'file_name': str(name),
        #                                                                             #'file_binary': attachment.encode('base64'),
        #                                                                         })

        # {
        #     "order_id":0,
        #     "sequence":"SOM00001",
        #     "partner_id":"13",
        #     "partner_invoice_id":"13",
        #     "partner_delivery_id":"13",
        #     "lines":[
        #         {
        #             "product_id":"7",
        #             "product_description":"CORE INTEL 9",
        #             "product_quantity":"3",
        #             "product_price":"547",
        #             "product_taxes":"1",
        #             "product_subservice":"91"
        #         },
        #         {
        #             "product_id":"4",
        #             "product_description":"Producto prueba nonupdated",
        #             "product_quantity":"2",
        #             "product_price":"10",
        #             "product_taxes":"1",
        #             "product_subservice":"96"
        #         }
        #     ]
        # }

        # [
        #     "text":"Referencia del pedido",
        #     "text":"Cliente/Nombre",
        #     "text":"Cliente/NIF",
        #     "text":"Dirección de entrega/NIF",
        #     "text":"Dirección de entrega/Nombre",
        #     "text":"Dirección de factura/NIF",
        #     "text":"Dirección de factura",
        #     "text":"Dirección de factura/Nombre",
        #     "text":"Líneas de Pedido/Cantidad",
        #     "text":"Líneas de Pedido/Impuestos/Código UNECE",
        #     "text":"Líneas de Pedido/Impuestos/Nombre del impuesto",
        #     "text":"Líneas de Pedido/Producto/Nombre",
        #     "text":"Líneas de Pedido/Producto/Referencia Interna",
        #     "text":"Líneas de Pedido/Producto/Código de Barras",
        #     "text":"Líneas de Pedido/SubServicios/Name",
        #     "text":"Líneas de Pedido/SubServicios/Parent Service"
        # ]

        # [
        #     {
        #         "Referencia del pedido":"SOM00001",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Dirección de entrega/NIF":"",
        #         "Dirección de entrega/Nombre":"Alex Grisales",
        #         "Dirección de factura/NIF":"",
        #         "Dirección de factura":"Alex Grisales",
        #         "Dirección de factura/Nombre":"Alex Grisales",
        #         "Líneas de Pedido/Cantidad":2.0,
        #         "Líneas de Pedido/Impuestos/Código UNECE":"Tarifa estándar",
        #         "Líneas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "Líneas de Pedido/Producto/Nombre":"CORE INTEL 9",
        #         "Líneas de Pedido/Producto/Referencia Interna":"CI9",
        #         "Líneas de Pedido/Producto/Código de Barras":"",
        #         "Líneas de Pedido/SubServicios/Name":"Next Day",
        #         "Líneas de Pedido/SubServicios/Parent Service":"Last Mile"
        #     },
        #     {
        #         "Referencia del pedido":"",
        #         "Cliente/Nombre":"",
        #         "Cliente/NIF":"",
        #         "Dirección de entrega/NIF":"",
        #         "Dirección de entrega/Nombre":"",
        #         "Dirección de factura/NIF":"",
        #         "Dirección de factura":"",
        #         "Dirección de factura/Nombre":"",
        #         "Líneas de Pedido/Cantidad":4.0,
        #         "Líneas de Pedido/Impuestos/Código UNECE":"Tarifa estándar",
        #         "Líneas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "Líneas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "Líneas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "Líneas de Pedido/Producto/Código de Barras":"78974W54",
        #         "Líneas de Pedido/SubServicios/Name":"Regular",
        #         "Líneas de Pedido/SubServicios/Parent Service":"General"
        #     },
        #     {
        #         "Referencia del pedido":"SOM00030",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Dirección de entrega/NIF":"",
        #         "Dirección de entrega/Nombre":"Alex Grisales",
        #         "Dirección de factura/NIF":"",
        #         "Dirección de factura":"Alex Grisales",
        #         "Dirección de factura/Nombre":"Alex Grisales",
        #         "Líneas de Pedido/Cantidad":1.0,
        #         "Líneas de Pedido/Impuestos/Código UNECE":"Tarifa estándar",
        #         "Líneas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "Líneas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "Líneas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "Líneas de Pedido/Producto/Código de Barras":"78974W54",
        #         "Líneas de Pedido/SubServicios/Name":"Regular",
        #         "Líneas de Pedido/SubServicios/Parent Service":"General"
        #     },
        #     {
        #         "Referencia del pedido":"SOM00029",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Dirección de entrega/NIF":"",
        #         "Dirección de entrega/Nombre":"Alex Grisales",
        #         "Dirección de factura/NIF":"",
        #         "Dirección de factura":"Alex Grisales",
        #         "Dirección de factura/Nombre":"Alex Grisales",
        #         "Líneas de Pedido/Cantidad":1.0,
        #         "Líneas de Pedido/Impuestos/Código UNECE":"Tarifa estándar",
        #         "Líneas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "Líneas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "Líneas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "Líneas de Pedido/Producto/Código de Barras":"78974W54",
        #         "Líneas de Pedido/SubServicios/Name":"Regular",
        #         "Líneas de Pedido/SubServicios/Parent Service":"General"
        #     }
        # ]

    #def get_column_position()

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