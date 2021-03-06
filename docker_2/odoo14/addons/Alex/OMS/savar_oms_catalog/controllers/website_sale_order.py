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
        #                                                                             'name': str('Importaci??n ') + str(fields.datetime.now()),
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
        #     "text":"Direcci??n de entrega/NIF",
        #     "text":"Direcci??n de entrega/Nombre",
        #     "text":"Direcci??n de factura/NIF",
        #     "text":"Direcci??n de factura",
        #     "text":"Direcci??n de factura/Nombre",
        #     "text":"L??neas de Pedido/Cantidad",
        #     "text":"L??neas de Pedido/Impuestos/C??digo UNECE",
        #     "text":"L??neas de Pedido/Impuestos/Nombre del impuesto",
        #     "text":"L??neas de Pedido/Producto/Nombre",
        #     "text":"L??neas de Pedido/Producto/Referencia Interna",
        #     "text":"L??neas de Pedido/Producto/C??digo de Barras",
        #     "text":"L??neas de Pedido/SubServicios/Name",
        #     "text":"L??neas de Pedido/SubServicios/Parent Service"
        # ]

        # [
        #     {
        #         "Referencia del pedido":"SOM00001",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Direcci??n de entrega/NIF":"",
        #         "Direcci??n de entrega/Nombre":"Alex Grisales",
        #         "Direcci??n de factura/NIF":"",
        #         "Direcci??n de factura":"Alex Grisales",
        #         "Direcci??n de factura/Nombre":"Alex Grisales",
        #         "L??neas de Pedido/Cantidad":2.0,
        #         "L??neas de Pedido/Impuestos/C??digo UNECE":"Tarifa est??ndar",
        #         "L??neas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "L??neas de Pedido/Producto/Nombre":"CORE INTEL 9",
        #         "L??neas de Pedido/Producto/Referencia Interna":"CI9",
        #         "L??neas de Pedido/Producto/C??digo de Barras":"",
        #         "L??neas de Pedido/SubServicios/Name":"Next Day",
        #         "L??neas de Pedido/SubServicios/Parent Service":"Last Mile"
        #     },
        #     {
        #         "Referencia del pedido":"",
        #         "Cliente/Nombre":"",
        #         "Cliente/NIF":"",
        #         "Direcci??n de entrega/NIF":"",
        #         "Direcci??n de entrega/Nombre":"",
        #         "Direcci??n de factura/NIF":"",
        #         "Direcci??n de factura":"",
        #         "Direcci??n de factura/Nombre":"",
        #         "L??neas de Pedido/Cantidad":4.0,
        #         "L??neas de Pedido/Impuestos/C??digo UNECE":"Tarifa est??ndar",
        #         "L??neas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "L??neas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "L??neas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "L??neas de Pedido/Producto/C??digo de Barras":"78974W54",
        #         "L??neas de Pedido/SubServicios/Name":"Regular",
        #         "L??neas de Pedido/SubServicios/Parent Service":"General"
        #     },
        #     {
        #         "Referencia del pedido":"SOM00030",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Direcci??n de entrega/NIF":"",
        #         "Direcci??n de entrega/Nombre":"Alex Grisales",
        #         "Direcci??n de factura/NIF":"",
        #         "Direcci??n de factura":"Alex Grisales",
        #         "Direcci??n de factura/Nombre":"Alex Grisales",
        #         "L??neas de Pedido/Cantidad":1.0,
        #         "L??neas de Pedido/Impuestos/C??digo UNECE":"Tarifa est??ndar",
        #         "L??neas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "L??neas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "L??neas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "L??neas de Pedido/Producto/C??digo de Barras":"78974W54",
        #         "L??neas de Pedido/SubServicios/Name":"Regular",
        #         "L??neas de Pedido/SubServicios/Parent Service":"General"
        #     },
        #     {
        #         "Referencia del pedido":"SOM00029",
        #         "Cliente/Nombre":"Alex Grisales",
        #         "Cliente/NIF":"",
        #         "Direcci??n de entrega/NIF":"",
        #         "Direcci??n de entrega/Nombre":"Alex Grisales",
        #         "Direcci??n de factura/NIF":"",
        #         "Direcci??n de factura":"Alex Grisales",
        #         "Direcci??n de factura/Nombre":"Alex Grisales",
        #         "L??neas de Pedido/Cantidad":1.0,
        #         "L??neas de Pedido/Impuestos/C??digo UNECE":"Tarifa est??ndar",
        #         "L??neas de Pedido/Impuestos/Nombre del impuesto":"18%",
        #         "L??neas de Pedido/Producto/Nombre":"Producto prueba nonupdated",
        #         "L??neas de Pedido/Producto/Referencia Interna":"PTEST",
        #         "L??neas de Pedido/Producto/C??digo de Barras":"78974W54",
        #         "L??neas de Pedido/SubServicios/Name":"Regular",
        #         "L??neas de Pedido/SubServicios/Parent Service":"General"
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