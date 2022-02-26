from odoo import api, fields, models
from dateutil import relativedelta as rdelta
from datetime import datetime, date, time, timedelta
from odoo.exceptions import ValidationError
import math
class HRLeaveInherit(models.Model):
    _inherit = "hr.leave"


    number_of_days = fields.Float(readonly=True)

    number_of_days_calendar = fields.Float(string='Duración Días Calendario', compute='method_compute_number_of_days_calendar')

    @api.depends('employee_id')
    def _compute_from_employee_id(self):
        for holiday in self:
            holiday.manager_id = holiday.employee_id.parent_id.id
            """
            if holiday.employee_id.user_id != self.env.user and self._origin.employee_id != holiday.employee_id:
                holiday.holiday_status_id = False
            """

    @api.depends('date_from', 'date_to', 'employee_id')
    def method_compute_number_of_days_calendar(self):
        for holiday in self:
            if holiday.date_from and holiday.date_to:
                rd = rdelta.relativedelta(holiday.request_date_to,holiday.request_date_from)
                holiday.number_of_days_calendar = rd.years*360 + rd.months*30 + rd.days + 1
            else:
                holiday.number_of_days_calendar = 0

    @api.model
    def create(self, vals):
        my_id = super(HRLeaveInherit, self).create(vals)
        employee_id = self.env['hr.employee'].search([('id','=',vals['employee_id'])])
        
        contract_ids = self.env['hr.contract'].search([('employee_id','=',vals['employee_id']),('state','in',['open','close'])])
        flag = False
        for contract_id in contract_ids:
            print(type(vals['request_date_from']),type(vals['request_date_to']) )
            if contract_id.date_start < fields.Date.from_string(vals['request_date_from']) and (not contract_id.date_end or contract_id.date_end > fields.Date.from_string(vals['request_date_to'])) :
                flag = True
                break
        if flag == False:
            raise ValidationError('No puede crear Ausencias en periodos donde no hay contrato asignado')
        return my_id


class HRLeaveTypeInherit(models.Model):
    _inherit = "hr.leave.type"


    days_considered = fields.Selection(
        string="Días Tomados",
        selection=[
            ('days_business', 'Días Laborales'),
            ('days_calendar', 'Días Calendarios'),
        ], default="days_business"
    )