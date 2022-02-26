# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from dateutil import relativedelta
import calendar

    
class employee(models.Model):
    _inherit = "hr.employee"
    """
    def AverageWageBiannual(self,date_to,list_codes,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
        if struct_id:
            struct = struct_id.id
            date_start = date_to + relativedelta.relativedelta(months=-5)
            date_from = date(date_start.year,date_start.month,1)
            payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
            amount=0
            days=0
            count=0
            list_wage= []
            list_amount= []
            list_days= []


            if payslips:
                for payslip in payslips:
                    flag=False
                    for line in payslip.line_ids:
                        if line.code in list_codes:
                            amount += line.total
                            list_amount.append(amount)
                            break

                    for line in payslip.worked_days_line_ids:
                        if line.work_entry_type_id.code == 'DIAT':
                            days += line.number_of_days
                            list_days.append(days)
                            break
                    salary_contract = amount*30/days
                    list_wage.append(salary_contract) 
                    amount = 0
                    days = 0

            sum_salary = 0

            for salary in list_wage:
                sum_salary +=salary

            average_salary = sum_salary/len(list_wage)

            if len(list_wage) <= 3:
                return average_salary
            elif list_wage[0]==list_wage[1]==list_wage[2]:

                return list_wage[0]
            else:   
                return average_salary

    
    def MethodAverageBiannual(self,date_to,list_codes,contract_id):
       type_struct_id = contract_id.structure_type_id.id
       struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
       if struct_id:
           struct = struct_id.id
           date_start = date_to + relativedelta.relativedelta(months=-5)
           date_from = date(date_start.year,date_start.month,1)
           payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
           amount=0
           list_amount= []
           print(len(payslips))
           if payslips:
               for payslip in payslips:
                   flag=False
                   amount=0
                   for line in payslip.line_ids:
                       if line.code in list_codes:
                           amount += line.total
                   
                   list_amount.append(amount)

           sum_category = 0

           for category in list_amount:
               sum_category +=category

           average_category = sum_category/len(list_amount)

           return average_category
       else:
           return 0
    """
    def GetWorkedDays(self,date_to,contract_id):
       type_struct_id = contract_id.structure_type_id.id
       struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
       days=0
       if struct_id:
           struct = struct_id.id
           date_start = date_to + relativedelta.relativedelta(months=-5)
           date_from = date(date_start.year,date_start.month,1)
           payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_from','<',date_to),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
           for payslip in payslips:
               for line in payslip.worked_days_line_ids:
                       if line.work_entry_type_id.code == 'DIAT':
                           days += line.number_of_days
       return days
                


    