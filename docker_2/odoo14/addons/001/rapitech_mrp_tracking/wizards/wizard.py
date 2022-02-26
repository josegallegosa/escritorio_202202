# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import UserError

class MrpProductProduceAll(models.TransientModel):
    _name = "mrp.product.produce.all"
    _description = "Wizard para ejecución de producción masiva"

    production_id = fields.Many2one('mrp.production', 'Manufacturing Order', required=True)
    product_id = fields.Many2one(related='production_id.product_id', readonly=True, store=True, string="Producto")
    qty_producing = fields.Float(string='Cantidad total', digits='Product Unit of Measure')
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', required=True, readonly=True)
    
    qty_producing_total = fields.Float('Cantidad a producir',required=True)
    company_id = fields.Many2one(related='production_id.company_id')

    @api.model
    def default_get(self, fields):
        res = super(MrpProductProduceAll, self).default_get(fields)
        production = self.env['mrp.production']
        production_id = self.env.context.get('default_production_id') or self.env.context.get('active_id')
        if production_id:
            production = self.env['mrp.production'].browse(production_id)
        if production.exists():
            todo_uom = production.product_uom_id.id
            todo_quantity = self._get_todo(production)
            if production.product_uom_id.uom_type != 'reference':
                todo_uom = self.env['uom.uom'].search([('category_id', '=', production.product_uom_id.category_id.id), ('uom_type', '=', 'reference')]).id
            if 'production_id' in fields:
                res['production_id'] = production.id
            if 'product_id' in fields:
                res['product_id'] = production.product_id.id
            if 'product_uom_id' in fields:
                res['product_uom_id'] = todo_uom
            if 'qty_producing' in fields:
                res['qty_producing'] = todo_quantity
            if 'qty_producing_total' in fields:
                res['qty_producing_total'] = todo_quantity
        return res

    def _get_todo(self, production):
        main_product_moves = production.move_finished_ids.filtered(lambda x: x.product_id.id == production.product_id.id)
        todo_quantity = production.product_qty - sum(main_product_moves.mapped('quantity_done'))
        todo_quantity = todo_quantity if (todo_quantity > 0) else 0
        return todo_quantity

    def do_produce(self):
        for i in range(int(self.qty_producing_total)):
            obj_wz = self.env['mrp.product.produce']
            production = self.env['mrp.production']
            production_id = self.env.context.get('default_production_id') or self.env.context.get('active_id')
            if production_id:
                production = self.env['mrp.production'].browse(production_id)
            if production.exists():
                todo_uom = production.product_uom_id.id
                if production.product_uom_id.uom_type != 'reference':
                    todo_uom = self.env['uom.uom'].search([('category_id', '=', production.product_uom_id.category_id.id), ('uom_type', '=', 'reference')]).id
                vals = {
                    'production_id':production.id,
                    'product_id':production.product_id.id,
                    'product_uom_id':todo_uom,
                    'qty_producing':1,
                    'consumption':production.bom_id.consumption,
                    'finished_lot_id':False,
                    'serial':True
                }
                obj_wz_id =obj_wz.create(vals)
                line_values = obj_wz_id._update_workorder_lines()
                active_tracking = 0
                lot = False

                for values in line_values['to_create']:
                    self.env['mrp.product.produce.line'].create(values)
                    if self.env['product.product'].browse(values['product_id']).product_tmpl_id.tracking_product:
                        active_tracking = active_tracking + 1
                        if values['lot_id']:
                            lot =  self.env['stock.production.lot'].browse(values['lot_id'])
                if active_tracking != 1:
                    raise UserError('No existen componentes con seguimiento o existen mas de un componente con seguimiento dentro de la lista de materiales')
                value = False 
                if lot:
                    value = self.env['stock.production.lot'].search([('product_id.id', '=', self.product_id.id),
                                                                     ('name', '=', lot.name),
                                                                     ('company_id', '=', self.company_id.id)],
                                                                    limit=1)
                if not value:
                    value = self.env['stock.production.lot'].create({
                        'product_id': self.product_id.id,
                        'company_id': self.company_id.id,
                        'name': lot.name
                    })

                obj_wz_id.write({'finished_lot_id':value.id})
                obj_wz_id._record_production()
                obj_wz_id._check_company()