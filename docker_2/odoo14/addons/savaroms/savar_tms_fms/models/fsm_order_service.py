from odoo import models, fields, api, _

class FsmOrderService(models.Model):
    _name = 'fsm.order.service'
    
    name = fields.Char(string='Subservicio')
    description = fields.Text(string='Descripción')
    parent_id = fields.Many2one('fsm.order.service', string='Servicio Padre')