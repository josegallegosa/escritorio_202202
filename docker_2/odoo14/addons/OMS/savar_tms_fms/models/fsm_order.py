from odoo import api, fields, models


class FsmOrder(models.Model):
    _inherit = 'fsm.order'

    service_id = fields.Many2one('fsm.order.service', string='Servicio')
    subservice_id = fields.Many2one(
        'fsm.order.service', string='Subservicio')
