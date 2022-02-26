from odoo import api, fields, models


class OmsPricelist(models.Model):
    _name = 'oms.pricelist'
    _description = 'New Description'

    name = fields.Char(string='Nombre', required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    service_id = fields.Many2one('fsm.order.service', string='Currency', required=True)
    service_name = fields.Char(string='Servicio', related='service_id.name')

    pricelist_item1_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='General')
    pricelist_item2_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Last Mile')
    pricelist_item3_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='FulFillment')
    pricelist_item4_ids = fields.One2many('oms.pricelist.item', 'pricelist_id', string='Consolidado')
    
    
    """
    @api.onchange('service_id')
    def compute_name_id(self):
        for rec in self:
            for item in rec.pricelist_item_ids:
                item.service_id = self.service_id.id
                print(f'item {item.service_id}')
            print(f'name {self.service_id.name}')
            self.name = f'name {self.service_id.name}'

    
    @api.depends('service_id')
    def compute_service_id(self):
        self.ensure_one()
        self.pricelist_item_ids.service_id.name =  f'name {self.service_id.name}'
        print(f'name {self.service_id.name}')
        #elf.name = f'name {self.service_id.name}'
    """ 