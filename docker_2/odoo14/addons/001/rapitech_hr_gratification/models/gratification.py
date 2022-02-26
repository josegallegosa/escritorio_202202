# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from datetime import datetime, date, time, timedelta
import calendar


class HrPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    bool_gratification = fields.Boolean('Estructura para Gratificación', default=True)


class employee(models.Model):
    _inherit = "hr.employee"

    def ComputeDaysDiscount(self,date_from,date_to,contract_id):
        struct_id = self.env.ref('hr_payroll_rg.structure_r_g').id
        payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id),('employee_id', '=', contract_id.employee_id.id)])
        count=0
        if payslips:
            for payslip in payslips:
                for line in payslip.worked_days_line_ids:
                    if line.work_entry_type_id.code in ('FALT','CSGO'):
                        count += line.number_of_days
        return count
        
    def GetMonthGrat(self,date_from,date_to,date_start):
        print ('entrooooooooooooooooooooooooooooooooooo',date_from,type(date_to),date_start)
        last_day = date(int(date_to.year),int(date_to.month),1)
        print ('=======================',last_day)
        month = 0
        if date_start <= date_from:
            print ('11111111111111111111111')
            month = 6
        elif date_start>last_day:
            print ('2222222222222222222222222222')
            month = 0
        else:
            print ('3333333333333333333333333333333333')
            month = int(date_to.month)-int(date_start.month)
        print ('*********', month)
        return month


    def AverageBC(self,date_from,date_to,contract_id):
        struct_id = self.env.ref('hr_payroll_rg.structure_r_g').id
        print ('*************',struct_id)
        payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id),('employee_id', '=', contract_id.employee_id.id)])
        bcar=0
        count=0
        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.code=='BCAR':
                        bcar += line.total
                count+=1
        return bcar/count if count>0 else 0

    def AverageHE(self,date_from,date_to,contract_id):
        struct_id = self.env.ref('hr_payroll_rg.structure_r_g').id
        print ('*************',struct_id)
        payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id),('employee_id', '=', contract_id.employee_id.id)])
        he=0
        count=0
        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.code in ('HE25','HE35','HE10'):
                        he += line.total
                count+=1
        return he/count if count>0 else 0