# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    is_product_tracking = fields.Boolean(string='is tracking bom', compute="_get_product_tracking")

    @api.depends('product_id','bom_id')
    def _get_product_tracking(self):
        for prod in self:
            res = False
            if prod.product_id.product_tmpl_id.tracking == 'serial':
                for bom in prod.bom_id.bom_line_ids:
                    if bom.product_id.product_tmpl_id.tracking_product:
                        res = True
            prod.is_product_tracking = res


    def open_produce_product_all(self):
        self.ensure_one()
        if self.bom_id.type == 'phantom':
            raise UserError('No puede producir un MO con un producto de kit LdM.')
        action = self.env.ref('rapitech_mrp_tracking.act_mrp_product_produce_all').read()[0]
        return action
