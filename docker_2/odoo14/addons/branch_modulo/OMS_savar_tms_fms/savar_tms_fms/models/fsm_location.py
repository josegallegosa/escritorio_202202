from odoo import api, fields, models


class FsmLocation(models.Model):
    _inherit = 'fsm.location'

    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
