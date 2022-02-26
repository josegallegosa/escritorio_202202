from odoo import models, fields, api



class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    oms_pricelist_id = fields.Many2one('oms.pricelist', string='Tarifa')

    seller_id = fields.Many2one('res.partner', string='Vendedor')
    type_order_id = fields.Many2one('type.order', string='Tipo de orden')
    
    """
    @api.onchange('oms_pricelist_id')
    def _onchange_oms_pricelist_id(self):
        for line in self.order_line:
            line._onchange_pricelist_fields()
    """

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    product_service_subservices = fields.Many2many(string='SubServicios',related='product_id.product_service_subservices')

    subservice_id = fields.Many2one('fsm.order.service', string='SubServicio')
    warehouse_id = fields.Many2one('stock.warehouse', string='Local')
    district_id = fields.Many2one('res.district', string='Zona')
    size_id = fields.Many2one('product.size', string='Talla')
    size_quant = fields.Integer(string='Cantidad Talla')     
    

    """
    @api.onchange('seller_id', 'subservice_id', 'warehouse_id', 'district_id', 'size_id', 'size_quant')
    def _onchange_pricelist_fields(self):
        price = self.order_id.oms_pricelist_id.get_pricelist_item_price(self.seller_id, self.subservice_id, self.warehouse_id, self.district_id, self.size_id, self.size_quant)
        self.price_unit = price
    """