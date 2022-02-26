# -*- coding: utf-8 -*-
from odoo import http, fields
import json


class QaLocationWorld(http.Controller):
    @http.route('/locationworld/transfer', type='json', auth='public')
    def index(self, datos):
        # result = []
        var = []
        valores = ""
        passed = False
        cantidad = len(datos)
        transferD = False
        error = False
        serie1 = False
        tipo1 = False
        serie2 = False
        tipo2 = False
        if cantidad == 1:
            try:
                if not datos[0]['serie'] == "":
                    serie1 = True
                else:
                    valores = "Serie"
                datos[0]['serie']
            except:
                valores = "Serie"
            try:
                if not datos[0]['tipo'] == "":
                    tipo1 = True
                else:
                    valores = valores + " tipo"
                datos[0]['tipo']

            except:
                valores = valores + " tipo"
        if cantidad == 2:
            try:
                if not datos[0]['serie'] == "":
                    serie1 = True
                else:
                    serie1 = False
                    valores = "serie - 1"
                datos[0]['serie']
            except:
                valores = "serie - 1"
            try:
                if not datos[0]['tipo'] == "":
                    tipo1 = True
                else:
                    tipo1 = False
                    valores = valores + " tipo - 1"
                datos[0]['tipo']
            except:
                valores = valores + " tipo - 1"
            try:
                if not datos[1]['serie'] == "":
                    serie2 = True
                else:
                    serie2 = False
                    valores = valores + " serie - 2"
                datos[1]['serie']
            except:
                valores = " serie - 2"
            try:
                if not datos[1]['tipo'] == "":
                    tipo2 = True
                else:
                    tipo2 = False
                    valores = valores + " tipo - 2"
                datos[1]['tipo']
            except:
                valores = valores + " tipo - 2"
        for rec in datos:
            if (serie1 and tipo1 and cantidad == 1) or (serie1 and tipo1 and serie2 and tipo2 and cantidad == 2):
                if cantidad == 2:
                    if datos[0]['tipo'].upper() == 'E' and datos[1]['tipo'].upper() == 'S':
                        var1 = http.request.env['stock.production.lot'].sudo().search(
                            [('name', '=', datos[0]['serie'])])
                        var2 = http.request.env['stock.production.lot'].sudo().search(
                            [('name', '=', datos[1]['serie'])])
                        if var1 and var2:
                            passed = True
                        else:
                            fallo = ""
                            if not var1:
                                fallo = datos[0]['serie']
                            if not var2:
                                fallo = datos[1]['serie']
                            response = {
                                'name': fallo,
                                'status': False,
                                'code': '17',
                                'message': 'La serie no Existe dentro de los registros'
                            }
                            return response
                        if datos[0]['serie'] == datos[1]['serie']:
                            response = {
                                'name': datos[0]['serie'],
                                'status': False,
                                'code': '21',
                                'message': 'No se puede realizar mantenimiento con la misma serie'
                            }
                            return response
                if cantidad == 1 and datos[0]['tipo'].upper() == 'E':
                    passed = True
                if passed:
                    var = http.request.env['stock.production.lot'].sudo().search(
                        [('name', '=', rec['serie'])])
                    if var:
                        for res in var:
                            response = {}
                            if error and len(datos) > 1:
                                response = {
                                    'name': rec['serie'],
                                    'status': False,
                                    'code': '19',
                                    'message': 'La Operación es Invalida'
                                }
                                return response
                            tipo = 'Transferencias internas'
                            if res.product_id:
                                # si es E -->origen si es S es destino
                                quant = http.request.env['stock.quant'].sudo().search(
                                    [('product_id', '=', res.product_id.id), ('quantity', '>', '0'),
                                     ('company_id', '=', res.company_id.id), ('lot_id', '=', var.id)])
                            if quant:
                                # Almacen Padre
                                code = quant.location_id.display_name.find('/')
                                if code > 0:
                                    super_location = http.request.env['stock.location'].sudo().search(
                                        [('name', 'like', quant.location_id.display_name[:code]),
                                         ('company_id', '=', res.company_id.id)])
                                    almacen = http.request.env['stock.warehouse'].sudo().search(
                                        [('view_location_id', '=', super_location.id),
                                         ('company_id', '=', res.company_id.id)])
                            if almacen:
                                # si es E destino--> si es S es origen
                                tranfer_type = http.request.env['stock.picking.type'].sudo().search(
                                    [('name', '=', tipo),
                                     ('warehouse_id', '=',
                                      almacen.id),
                                     ('company_id', '=',
                                      res.company_id.id)])
                                if rec['tipo'].upper() == 'E':
                                    destino_lot = http.request.env['stock.location'].sudo().search(
                                        [('name', 'like', 'CLIENTES'),
                                         ('location_id', '=', super_location.id),
                                         ('company_id', '=', res.company_id.id)])
                                else:
                                    if rec['tipo'].upper() == 'S' and transferD:
                                        destino_lot = http.request.env['stock.location'].sudo().search(
                                            [('name', 'like', 'T. Stock'),
                                             ('location_id', '=', transferD.location_id.location_id.id),
                                             ('company_id', '=', res.company_id.id)])
                                    else:
                                        error = True
                                        response = {
                                            'name': rec['serie'],
                                            'status': False,
                                            'code': '19',
                                            'message': 'La Operación es Invalida'
                                        }
                                        break
                            else:
                                response = {
                                    'name': rec['serie'],
                                    'status': False,
                                    'code': '11',
                                    'message': 'No se pudo localizar el Almacen de Origen'
                                }
                                return response
                            if not tranfer_type:
                                response = {
                                    'name': rec['serie'],
                                    'status': False,
                                    'code': '13',
                                    'message': 'No se pudo localizar el Tipo de transferencia'
                                }
                                return response
                            else:
                                if destino_lot.id == quant.location_id.id:
                                    response = {
                                        'name': rec['serie'],
                                        'status': False,
                                        'code': '18',
                                        'message': 'La Serie ya fue Tranferida al almacen ' + destino_lot.display_name
                                    }
                                    return response
                                else:
                                    if destino_lot:
                                        prepare_values = {"state": "draft",
                                                          "picking_type_id": tranfer_type.id,
                                                          "company_id": res.company_id.id,
                                                          "location_id": quant.location_id.id,
                                                          "location_dest_id": destino_lot.id,
                                                          # "scheduled_date": fields.Datetime,
                                                          "move_ids_without_package": [{"origin": "",
                                                                                        "product_uom_qty": 1,
                                                                                        "quantity_done": 1,
                                                                                        "company_id": res.company_id.id,
                                                                                        "location_id": quant.location_id.id,
                                                                                        "product_uom": res.product_uom_id.id,
                                                                                        "name": " ",
                                                                                        "product_id": res.product_id.id,
                                                                                        "picking_type_id": tranfer_type.id,
                                                                                        "location_dest_id": destino_lot.id}]
                                                          }
                                        try:
                                            record = http.request.env['stock.picking'].sudo().create(prepare_values)
                                        except:
                                            record = False
                                            response = {
                                                'name': rec['serie'],
                                                'status': False,
                                                'code': '14',
                                                'message': 'Error al crear Registro'
                                            }
                                        if record:
                                            record.action_confirm()
                                            try:
                                                assign = record.action_assign()
                                            except:
                                                assign = False
                                                response = {
                                                    'name': rec['serie'],
                                                    'status': False,
                                                    'code': '15',
                                                    'message': 'No se encontro stock disponible'
                                                }
                                            if assign:
                                                record.move_line_ids_without_package.lot_id = res.id
                                            try:
                                                record.button_validate()
                                                validate = True
                                                if validate and rec['tipo'].upper() == 'E':
                                                    transferD = record
                                                    response = {
                                                        'name': record.name,
                                                        'status': True,
                                                        'code': '20',
                                                        'message': 'Transferencia exitosa'
                                                    }
                                                elif validate and rec['tipo'].upper() == 'S':
                                                    response = {
                                                        'name': transferD.name + ', ' + record.name,
                                                        'status': True,
                                                        'code': '20',
                                                        'message': 'Transferencia exitosa'
                                                    }
                                            except:
                                                response = {
                                                    'name': rec['serie'],
                                                    'status': False,
                                                    'code': '16',
                                                    'message': 'No se pudo Validar la transferencia'
                                                }
                                    else:
                                        response = {
                                            'name': rec['serie'],
                                            'status': False,
                                            'code': '12',
                                            'messaeg': 'No se pudo localizar el Almacen de Destino'
                                        }
                                        return response
                    else:
                        response = {
                            'name': rec['serie'],
                            'status': False,
                            'code': '17',
                            'message': 'La serie no Existe dentro de los registros'
                        }
                else:
                    response = {
                        'name': '',
                        'status': False,
                        'code': '19',
                        'message': 'La Operación es Invalida'
                    }
                    return response
            else:
                response = {
                    'name': valores,
                    'status': False,
                    'code': '10',
                    'message': 'Campos enviados no contienen valor y/o no exiten'
                }
                return response
        return response

    #     @http.route('/qa_location_world/qa_location_world/objects/', auth='public')
    #     def list(self, **kw):
    #         return http.request.render('qa_location_world.listing', {
    #             'root': '/qa_location_world/qa_location_world',
    #             'objects': http.request.env['qa_location_world.qa_location_world'].search([]),
    #         })

    #     @http.route('/qa_location_world/qa_location_world/objects/<model("qa_location_world.qa_location_world"):obj>/', auth='public')
    #     def object(self, obj, **kw):
    #         return http.request.render('qa_location_world.object', {
    #             'object': obj
    #         })
