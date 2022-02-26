############################################################################################
# ** QUANAM
# ** AUTOR: QUANAM
# ** CAMBIOS: NUMERO     FECHA (DD/MM/YYYY)  PERSONA               CAMBIOS EFECTUADOS
# --          00001      30/10/2020          JOSE CONDORI          MODULO PRODUCIÓN AJUSTE
# --          00002      02/11/2020          JOSE CONDORI          MODULO FABRICACION DESARROLLO
############################################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = "stock.location"

    admin_id = fields.Char(string="ID ADMIN")
    check_list = fields.Boolean(string="Ubicación Seleccionable")


# INICIO 00010
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    tracking_product = fields.Boolean(string='Tracking Product')


# FIN 00010
# INICIO 00002
class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('bom_id')
    def _create_product(self):
        for rec in self:
            active_tracking = 0
            main_name = False
            main_lot = False
            if rec.bom_id:
                for line in rec.bom_id.bom_line_ids:
                    if line.product_tmpl_id.tracking_product:
                        active_tracking = active_tracking + 1
                        main_name = line.product_id.name
                        # main_lot =


class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    @api.onchange('raw_workorder_line_ids')
    def _get_lot_id(self):
        active_tracking = 0
        main_lot = False
        for rec in self:
            if rec.qty_producing == 1:
                if rec.raw_workorder_line_ids:
                    for line in rec.raw_workorder_line_ids:
                        if line.product_id.product_tmpl_id.tracking_product:
                            active_tracking = active_tracking + 1
                            main_lot = line.lot_id
            if active_tracking == 1 and not self.finished_lot_id:
                self.finished_lot_id = self._process_tracking_product()
            else:
                self.finished_lot_id = False

    @api.model
    def default_get(self, fields):
        rec = super(MrpProductProduce, self).default_get(fields)
        return rec

    def _get_tracking_product(self):
        self.ensure_one()
        valor = self.env['stock.production.lot']
        for line in self.raw_workorder_line_ids:
            if line.product_id.tracking_product:
                if line.lot_id:
                    valor = line.lot_id
        return valor

    def _process_tracking_product(self):
        self.ensure_one()
        value = self.env['stock.production.lot']
        lot = self._get_tracking_product()
        if lot:
            value = self.env['stock.production.lot'].search([('product_id.id', '=', self.product_id.id),
                                                             ('name', '=', lot.name),
                                                             ('company_id', '=', self.production_id.company_id.id)],
                                                            limit=1)
            if not value:
                value = self.env['stock.production.lot'].create({
                    'product_id': self.product_id.id,
                    'company_id': self.production_id.company_id.id,
                    'name': lot.name
                })
        return value

# FIN 00002
