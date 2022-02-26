# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from datetime import datetime,date,timedelta
from dateutil import relativedelta as rdelta


def roundBy(x, base=1.25):
    return int(base * round(float(x)/base))


class HolidaysAllocation(models.Model):
    """ Allocation Requests Access specifications: similar to leave requests """
    _inherit = "hr.leave.allocation"

    vacation_start = fields.Date(string='Fecha de inicio de generación de vacaciones')
    vacation_end = fields.Date(string='Fecha de fin de generación de vacaciones')


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    vacation_ids = fields.One2many(comodel_name='hr.leave.allocation', inverse_name='employee_id',string='Vacaciones')

    @api.model
    def cron_create_vacation(self):
        date_now = datetime.now().date()

        contracts_ids = self.env['hr.contract'].search([('state', '=', 'open')]).ids
        employee_ids = self.search([('contract_id','in',contracts_ids)])

        print (employee_ids,len(employee_ids))
        for employee in employee_ids:
           
            dif = rdelta.relativedelta(date_now,employee.contract_id.date_start)
            dif_months = dif.months + 12*dif.years
            dif_days = dif.days

            leave_type = self.env.ref('hr_social_benefits.holiday_leave_vdi')
                
            line = self.env['hr.leave.allocation'].search([('employee_id','=',employee.id),('holiday_status_id','=',leave_type.id)])
            if line:
                if dif_days:
                    line.write({'number_of_days':line.number_of_days_display+(1.25/30),
                        'vacation_end':date_now})
                else:
                    line.write({'number_of_days':roundBy(line.number_of_days_display),
                        'vacation_end':date_now})
            else:
                vacation_start = employee.contract_id.date_start
                
                dias = 1.25*dif_months+dif_days*(1.25/30)
                print ('**************************',dias)
                vals={'name':leave_type.name+' '+employee.name,
                'employee_id':employee.id,
                'holiday_status_id':leave_type.id,
                'vacation_start':vacation_start,
                'vacation_end':date_now,
                'number_of_days':1.25*dif_months+dif_days*(1.25/30)}
                line = self.env['hr.leave.allocation'].create(vals)

        
            
