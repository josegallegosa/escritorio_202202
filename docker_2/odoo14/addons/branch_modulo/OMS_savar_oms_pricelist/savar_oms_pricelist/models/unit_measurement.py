from odoo import api, fields, models


class UnitMeasurement(models.Model):
    _name = 'unit.measurement'
    _description = 'Unidad de Medida'

    name = fields.Char(string='Unidad de Medida')
    description = fields.Text(string='Descripción')
