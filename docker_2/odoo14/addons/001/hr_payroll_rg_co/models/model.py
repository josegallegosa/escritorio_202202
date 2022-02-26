# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime, date, time, timedelta
from dateutil import relativedelta
import calendar

    



class employee(models.Model):
    _inherit = "hr.employee"

    def GetIBCSLastMonth(self,date_to,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

        date_start = date_to + relativedelta.relativedelta(months=-12)
        date_from = date(date_start.year,date_start.month,1)

        payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

        ibs_last_month = 0
        if payslips:
          for payslip in payslips:
              for line in payslip.line_ids:
                  if line.code=='IBCS':
                      ibs_last_month += line.total
          if ibs_last_month/len(payslips) >0:
            return ibs_last_month/len(payslips)
        else:
          return contract_id.wage



    def GetBaseIndemnizacion(self,date_to,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

        date_start = date_to + relativedelta.relativedelta(months=-12)
        date_from = date(date_start.year,date_start.month,1)

        payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")


        base_indemnizacion = 0

        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.category_id.code=='HE' or line.category_id.code=='RC' or line.category_id.code=='EXT' :
                        base_indemnizacion += line.total
            if len(payslips) ==0:
                return 0
            else:    
                return base_indemnizacion/len(payslips)
        else:
          return 0

    def GetBaseVacCompensadas(self,date_to,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

        date_start = date_to + relativedelta.relativedelta(months=-12)
        date_from = date(date_start.year,date_start.month,1)

        payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

        base_vac_compensadas = 0

        print("payslips ", payslips)

        print("len payslips ", len(payslips))

        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.category_id.code=='HE' or line.category_id.code=='RC' or line.category_id.code=='EXT' :
                        base_vac_compensadas += line.total
            if len(payslips) ==0:
                return 0
            else: 
                return base_vac_compensadas/len(payslips)
        else:
          return 0
      
    def GetBaseVacDisfrutadas(self,date_to,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

        date_start = date_to + relativedelta.relativedelta(months=-12)
        date_from = date(date_start.year,date_start.month,1)

        payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

        base_vac_disfrutadas = 0

        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.category_id.code=='RC' or line.category_id.code=='EXT' :
                        base_vac_disfrutadas += line.total
            if len(payslips) ==0:
                return 0
            else: 
                return base_vac_disfrutadas/len(payslips)
        else:
          return 0

    def GetBaseVacPorRetiro(self,date_to,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

        date_start = date_to + relativedelta.relativedelta(months=-12)
        date_from = date(date_start.year,date_start.month,1)

        payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

        base_vac_por_retiro = 0

        if payslips:
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.category_id.code=='HE' or line.category_id.code=='RC' or line.category_id.code=='EXT' :
                        base_vac_por_retiro += line.total
            if len(payslips) ==0:
                return 0
            else: 
                return base_vac_por_retiro/len(payslips)
        else:
          return 0

    def GetRetentionAtTheSource(self,date_from,ilmu):

        uvt = self.env['hr.payroll.parameters.line'].get_amount('UVT',  date_from)

        ximp = 0

        retencion_obj = self.env["hr.retencion.line"]
             
        for scale in retencion_obj.get_scales_retencion():
            if scale['lower_limit'] == 0:
                ximp = 0
            elif ilmu >= scale['lower_limit'] and ilmu <= scale['upper_limit']:
                ximp = ((ilmu - scale['lower_limit'])*scale['percentage']/100 + scale['additional'])*uvt
        return ximp


    def GetInterestOfBaskets(self,date_to,contract_id):
        struct_id_cesa = self.env.ref('structure_layoffs.structure_cesa_co').id

        date_start = date_to + relativedelta.relativedelta(months=-1)
        date_from = date(date_start.year,date_start.month,1)

        payslips_cesa = self.env['hr.payslip'].sudo().search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id_cesa),
            ('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

        cesantia = 0
        dias = 0
        if payslips_cesa:
            if payslips_cesa.date_from.month == 1:
                for payslip in payslips_cesa:
                    for line in payslip.line_ids:
                        if line.category_id.code=='PRCE':
                            cesantia += line.total
                for payslip in payslips_cesa:
                    for line in payslip.line_ids:
                        if line.category_id.code=='DIAN':
                            dias += line.total
                return cesantia*0.12*dias/360
        else:
            return 0
     
    
    def AverageWageBiannual(self,date_to,list_codes,contract_id):
        type_struct_id = contract_id.structure_type_id.id
        struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
        if struct_id:
            struct = struct_id.id
            date_start = date_to + relativedelta.relativedelta(months=-5)
            date_from = date(date_start.year,date_start.month,1)
            payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")

            amount=0
            days=0
            count=0
            list_wage= []
            list_amount= []
            list_days= []

            list_wage.append(contract_id.wage)

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
                
        else:
          return 0


    def MethodAverageBiannual(self,date_to,list_codes,contract_id, amounts):
       type_struct_id = contract_id.structure_type_id.id
       struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
       if struct_id:
           struct = struct_id.id
           date_start = date_to + relativedelta.relativedelta(months=-5)
           date_from = date(date_start.year,date_start.month,1)
           payslips = self.env['hr.payslip'].search([('date_from','>=',date_from),('date_to','<',date_to),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
           amount=0
           list_amount= []
           for x in amounts:
            amount += x
           list_amount.append(amount)
            
           amount=0

           if payslips:
               for payslip in payslips:
                   print("payslips", payslip.period_id.name)
                   flag=False
                   amount=0
                   for line in payslip.line_ids:
                       if line.code in list_codes:
                           amount += line.total
                   
                   list_amount.append(amount)

           sum_category = 0

           print('list_amount ', list_amount)
           print('list_codes ',list_codes)
           for category in list_amount:
               sum_category +=category

           average_category = sum_category/len(list_amount)

           return average_category
       else:
           return 0

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
                       if line.work_entry_type_id.code in ('DIAT','INC','IGE','IRL','LMA','LPA','LR','LT'):
                           days += line.number_of_days
       return days

