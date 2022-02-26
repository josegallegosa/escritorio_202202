# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
import calendar


# date_start hr.contract - inicia trabajo 22/12/2020
# date_from hr_payslip - perido de nomina  01/05/2021

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    period_cts = fields.Selection(
        string="Perido de CTS",
        selection=[('none','Ninguno'),
            ('may', 'Mayo'),
            ('november', 'Noviembre'),
        ], default="none"
    )
    @api.onchange('period_cts','date_from','date_to','period_id')
    def _onchange_period_cts(self):
        if self.period_cts!='none' and self.period_id:
            if self.period_cts == 'may':
                self.date_from = date(self.period_id.date_start.year-1,11,1)
                self.date_to = date(self.period_id.date_end.year,4,30)
            elif self.period_cts == 'november':
                self.date_from = date(self.period_id.date_start.year,5,1)
                self.date_to = date(self.period_id.date_end.year,10,31)


class HrPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    bool_cts = fields.Boolean('CTS Activo', default=True)
    

class employee(models.Model):
    _inherit = "hr.employee"


    def ComputeDaysDiscount(self,date_from,date_to,contract_id):
        struct_id = self.env.ref('hr_payroll_rg.structure_r_g').id
        print ('*************',struct_id)
        payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id),('employee_id', '=', contract_id.employee_id.id)])
        count=0
        if payslips:
            for payslip in payslips:
                for line in payslip.worked_days_line_ids:
                    if line.work_entry_type_id.code in ('FALT','CSGO'):
                        count += line.number_of_days
        return count

    def GetGratification(self,date_from,date_to,contract_id):
        struct_id = self.env.ref('hr_payroll_rg.structure_r_g').id
        print ('*************',struct_id,date_from,date_to)
        payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id),('employee_id', '=', contract_id.employee_id.id)])
        gratification=0
        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.code=='GRAT':
                        gratification += line.total
        return gratification

    def CountDayCts(self,date_from,date_to,date_start,date_end):

        if date_start <= date_from:
            if not date_end == False:
                if date_end < date_to:
                    date_to = date_end
                    if (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 < 0:
                        return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 + 12 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
                    else:   
                        return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
            else:
                if (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 < 0:
                    return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 + 12 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
                else:   
                    return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31

        if date_start > date_from:
            date_from = date_start
            if not date_end == False:
                if date_end < date_to:
                    date_to = date_end
                    if (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 < 0:
                        return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 + 12 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
                    else:   
                        return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
            else:
                if (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 < 0:
                    return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 + 12 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
                else:   
                    return (date_to.day + 30-(date_from.day-1))//30+date_to.month-date_from.month-1 ,(date_to.day + 30-(date_from.day-1))%30-date_to.day//31
