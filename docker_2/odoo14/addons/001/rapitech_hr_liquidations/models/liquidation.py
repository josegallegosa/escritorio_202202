# -*- coding: utf-8 -*-
##############################################################################

from odoo import fields, models
from dateutil import relativedelta as rdelta
from datetime import datetime, date, time, timedelta
import calendar

class employee(models.Model):
    _inherit = "hr.employee"

MESES = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

class HrPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    bool_liquidation = fields.Boolean('Estructura para Liquidación', default=True)


class employee(models.Model):
    _inherit = "hr.employee"


    def _get_vacations_liq(self,date_of_admission,termination_date,employee):
        allocation_ids = self.env['hr.leave.allocation'].search([('holiday_status_id.is_vacation','=',True),
            ('employee_id','=',employee.id),('state','=','validate')])
        days=0
        days_lab = 0
        days_vac = 0
        rd = rdelta.relativedelta(termination_date,date_of_admission)
        if (rd.years*1+rd.months*30+rd.days+1)>0:
            days_lab = (rd.years*360+rd.months*30+rd.days+1)
            days_vac = days_lab*15/360
        print("days_vac ", days_vac)
        print("days ", days)
        date_vacation = ''
        prov = 0
        if allocation_ids:
            for allocation in allocation_ids:
                days += allocation.leaves_taken
            date_vacation = 'Del '+str(allocation_ids[0].vacation_start.day)+' de '+str(MESES[allocation_ids[0].vacation_start.month-1])+' del '+str(allocation_ids[0].vacation_start.year)+' al '+str(allocation_ids[0].vacation_end.day)+' de '+str(MESES[allocation_ids[0].vacation_end.month-1])+' del '+str(allocation_ids[0].vacation_end.year)

            prov = (days_vac-days)

        return prov, date_vacation

    def get_prima_liq(self,date_to,list_codes,contract_id):
       type_struct_id = contract_id.structure_type_id.id
       struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
       if struct_id:
           days = 0
           struct = struct_id.id

           date_end = date(date_to.year,date_to.month,1)
           
           if date_end >= date(date_to.year,6,1):
            date_start = date(date_to.year,6,1)
           else:
            date_start = date(date_to.year,1,1)

           rd = rdelta.relativedelta(date_to,date_start)
           days = rd.years*360 + rd.months*30 + rd.days

           payslips = self.env['hr.payslip'].search([('date_from','>=',date_start),('date_from','<',date_end),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
           amount=0
           list_amount= []
           average_category = 0
           print("len(payslips) ", len(payslips))
           if payslips:
               for payslip in payslips:
                   flag=False
                   for line in payslip.line_ids:
                       if line.code in list_codes:
                           amount += line.total
                   list_amount.append(amount)
                   amount = 0

               sum_category = 0

               for category in list_amount:
                   sum_category +=category

               average_category = sum_category/len(list_amount)

           return average_category , days
       else:
           return 0,0


    def get_cesantia_liq(self,date_to,list_codes,contract_id):
       type_struct_id = contract_id.structure_type_id.id
       struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)
       if struct_id:
           days = 0
           struct = struct_id.id
           
           date_end = date(date_to.year,date_to.month,1)
           
           if date_end >= date(date_to.year,6,1):
            date_start = date(date_to.year,6,1)
           else:
            date_start = date(date_to.year,1,1)
           
           rd = rdelta.relativedelta(date_to,date_start)
           days = rd.years*360 + rd.months*30 + rd.days + 1

           payslips = self.env['hr.payslip'].search([('date_from','>=',date_start),('date_from','<',date_end),('struct_id','=',struct_id.id),('employee_id', '=', contract_id.employee_id.id)], order="date_from desc")
           amount=0
           list_amount= []
           average_category = 0
           if payslips:
               for payslip in payslips:
                   flag=False
                   for line in payslip.line_ids:
                       if line.code in list_codes:
                           amount += line.total
                   list_amount.append(amount)
                   amount = 0
           
               sum_category = 0

               for category in list_amount:
                   sum_category +=category

               average_category = sum_category/len(list_amount)

           return average_category , days
       else:
           return 0,0

    """
    def _get_cts_liq(self,date_of_admission,termination_date,salary,contract_id):
        
        f_inicio_contrato = date_of_admission

        periodo1 = [11,12,1,2,3,4]
        periodo2 = [5,6,7,8,9,10]

        if termination_date.month in periodo1:
            if termination_date.month in (11,12):
                start_date = date(termination_date.year,11,1)
                #end_date = date(termination_date.year +1,4,30)
                l_per = periodo1
            else:
                start_date = date(termination_date.year - 1,11,1)
                #end_date = date(termination_date.year,4,30)
                l_per = periodo1
        if termination_date.month in periodo2:
            start_date = date(termination_date.year,5,1)
            #end_date = date(termination_date.year,10,31)
            l_per = periodo2
        if f_inicio_contrato <= start_date:
            if termination_date.month in l_per:
                mes = 0
                for p in l_per:
                    mes += 1
                    if p == termination_date.month:
                        break
            if termination_date.day in (30,31):
                months = mes
                days = 0
            else:
                months = mes-1
                days = termination_date.day


        else:
            if termination_date.day == 1:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == termination_date.month:
                            break
                days = 0
                months = mes 

            else:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == termination_date.month:
                            break
                days = termination_date.day
                months = mes -1

        m2payslip = f_inicio_contrato <= start_date and l_per or l_per[l_per.index(f_inicio_contrato.month):]

        faltas=0
        for m in m2payslip:
            if m in (11,12) and termination_date.month not in (11,12):
                initdate = date(termination_date.year-1,m,1)
                enddate = date(termination_date.year-1,m,calendar.monthrange(termination_date.year-1, m)[1] )
            else:
                initdate = date(termination_date.year,m,1)
                enddate = date(termination_date.year,m,calendar.monthrange(termination_date.year, m)[1] ) 

            faltas += self.ComputeDaysDiscount(initdate,enddate,contract_id)
        salary = salary

        if days == 0:
            prov = (abs(salary) / 12 * months)- (faltas * salary / 360 )

        else:
            prov = ( abs(salary) / 12 * months ) - ( (faltas-days)*salary/(12*30) )

        if m2payslip[0] in (11,12) and termination_date.month not in (11,12):
            txt_year = termination_date.year -1
        else:
            txt_year = termination_date.year

        txt = 'Del 1 de '+str(MESES[m2payslip[0]-1])+' del '+str(txt_year)+' al '+str(termination_date.day)+' de '+str(MESES[termination_date.month-1])+' del '+str(termination_date.year)
        txt = 'Del 1 de '+str(MESES[m2payslip[0]-1])+' del '+str(txt_year)+' al '+str(termination_date.day)+' de '+str(MESES[termination_date.month-1])+' del '+str(termination_date.year)
        return prov, months, days, txt


    def _get_gratification_liq(self,date_of_admission,termination_date,salary,contract_id):
        f_inicio_contrato = date_of_admission

        periodo1 = [1,2,3,4,5,6]
        periodo2 = [7,8,9,10,11,12]

        if termination_date.month in periodo1:
            start_date = date(termination_date.year,1,1)
            #end_date = date(termination_date.year,6,30)
            l_per = periodo1
        if termination_date.month in periodo2:
            start_date = date(termination_date.year,7,1)
            #end_date = date(termination_date.year,12,31)
            l_per = periodo2

        if f_inicio_contrato <= start_date:
            if termination_date.month in l_per:
                mes = 0
                for p in l_per:
                    mes += 1
                    if p == termination_date.month:
                        break
            if termination_date.day in (30,31):
                months = mes
                #days = 0
            else:
                months = mes-1
                #days = termination_date.day

        else:
            if termination_date.day == 1:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == termination_date.month:
                            break
                months = mes 

            else:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == termination_date.month:
                            break
                months = mes -1

        m2payslip = f_inicio_contrato <= start_date and l_per or l_per[l_per.index(f_inicio_contrato.month):]

        faltas=0
        for m in m2payslip:
            initdate = date(termination_date.year,m,1)
            enddate = date(termination_date.year,m,calendar.monthrange(termination_date.year, m)[1] ) 


            faltas += self.ComputeDaysDiscount(initdate,enddate,contract_id)

        salary = salary 

        prov = (abs(salary) / 6 * months) - (faltas * salary / 180 )

        return prov, months, 'Del 1 de '+str(MESES[m2payslip[0]-1])+' del '+str(termination_date.year)+' al '+str(termination_date.day)+' de '+str(MESES[termination_date.month-1])+' del '+str(termination_date.year)

    """