from odoo import api, fields, models


class OmsPricelist(models.Model):
    _name = 'oms.pricelist'
    _description = 'New Description'

    name = fields.Char(string='Nombre', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    service_id = fields.Many2one('fsm.order.service', string='Currency', required=True)
    service_name = fields.Char(string='Servicio', related='service_id.name')
    seller_id = fields.Many2one('res.partner', string='Vendedor')

    pricelist_item1_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='General')
    pricelist_item2_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Last Mile')
    pricelist_item3_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='FulFillment')
    pricelist_item4_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Consolidado')
    

    """
    def get_pricelist_item_price(self, seller_id, subservice_id, warehouse_id, district_id, size_id, size_quant):
        pricelist_item_id = self.env['oms.pricelist.item'].search([('pricelist_id', '=', self.id), ('seller_id', '=', seller_id.id), ('subservice_id', '=', subservice_id.id), (
        'warehouse_id', '=', warehouse_id.id), ('district_id', '=', district_id.id), ('size_id', '=', size_id.id), ('size_quant', '=', size_quant)], limit=1)
        return pricelist_item_id.price
    """