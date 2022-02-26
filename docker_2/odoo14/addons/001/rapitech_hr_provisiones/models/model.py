# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from datetime import datetime, date, time, timedelta
import calendar


class HrPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    bool_provision = fields.Boolean('Estructura para Provision', default=True)


class employee(models.Model):
    _inherit = "hr.employee"

    def GetPCTS(self,date_from,date_to,date_start,salary,contract_id):
        
        print(date_start)
        f_inicio_contrato = date_start

        periodo1 = [11,12,1,2,3,4]
        periodo2 = [5,6,7,8,9,10]

        if date_from.month in periodo1:
            if date_from.month in (11,12):
                start_date = date(date_from.year,11,1)
                end_date = date(date_from.year +1,4,30)
                l_per = periodo1
            else:
                start_date = date(date_from.year - 1,11,1)
                end_date = date(date_from.year,4,30)
                l_per = periodo1
        if date_from.month in periodo2:
            start_date = date(date_from.year,5,1)
            end_date = date(date_from.year,10,31)
            l_per = periodo2

        if f_inicio_contrato <= start_date:
            if date_from.month in l_per:
                mes = 0
                for p in l_per:
                    mes += 1
                    if p == date_from.month:
                        break
            months = mes
            days = 0


        else:
            if f_inicio_contrato.day == 1:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == date_from.month:
                            break
                days = 0
                months = mes 

            else:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == date_from.month:
                            break
                days = 30 - f_inicio_contrato.day
                months = mes -1

        m2payslip = f_inicio_contrato <= start_date and l_per or l_per[l_per.index(f_inicio_contrato.month):]

        struct_id = self.env.ref('rapitech_hr_provisiones.structure_employee_prov').id
        acumulado=0
        faltas=0
        for m in m2payslip:
            if m in (11,12) and date_from.month not in (11,12):
                initdate = date(date_from.year-1,m,1)
                enddate = date(date_from.year-1,m,calendar.monthrange(date_from.year-1, m)[1] )
            else:
                initdate = date(date_from.year,m,1)
                enddate = date(date_from.year,m,calendar.monthrange(date_from.year, m)[1] ) 

            payslips = self.env['hr.payslip'].search([('date_from','>=',initdate),
                ('date_to','<=',enddate),('struct_id','=',struct_id),
                ('employee_id', '=', contract_id.employee_id.id)])

            faltas += self.ComputeDaysDiscount(initdate,enddate,contract_id)

            if payslips:
                for payslip in payslips:
                    neto = 0
                    for line in payslip.line_ids:
                        if line.code=='PCTS':
                            acumulado += line.total
        salary = salary - (faltas * salary / 360 ) 

        if days == 0:
            prov = (abs(salary) / 12 * months) - acumulado

        else:
            prov = ( abs(salary) / 12 * months ) - ( (30-days*salary)/(12*30) ) - acumulado

        return prov

    def GetPGRAT(self,date_from,date_to,date_start,salary,contract_id):
        print(date_start)
        f_inicio_contrato = date_start

        periodo1 = [1,2,3,4,5,6]
        periodo2 = [7,8,9,10,11,12]

        if date_from.month in periodo1:
            start_date = date(date_from.year,1,1)
            end_date = date(date_from.year,6,30)
            l_per = periodo1
        if date_from.month in periodo2:
            start_date = date(date_from.year,7,1)
            end_date = date(date_from.year,12,31)
            l_per = periodo2

        if f_inicio_contrato <= start_date:
            if date_from.month in l_per:
                mes = 0
                for p in l_per:
                    mes += 1
                    if p == date_from.month:
                        break
            months = mes

        else:
            if f_inicio_contrato.day == 1:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == date_from.month:
                            break
                months = mes 

            else:
                m_val = l_per.index(f_inicio_contrato.month)
                if f_inicio_contrato.month in l_per:
                    mes = 0
                    for p in l_per[m_val:]:
                        mes += 1
                        if p == date_from.month:
                            break
                months = mes -1

        m2payslip = f_inicio_contrato <= start_date and l_per or l_per[l_per.index(f_inicio_contrato.month):]

        struct_id = self.env.ref('rapitech_hr_provisiones.structure_employee_prov').id
        acumulado=0
        faltas=0
        for m in m2payslip:
            initdate = date(date_from.year,m,1)
            enddate = date(date_from.year,m,calendar.monthrange(date_from.year, m)[1] ) 

            payslips = self.env['hr.payslip'].search([('date_from','>=',initdate),
                ('date_to','<=',enddate),('struct_id','=',struct_id),
                ('employee_id', '=', contract_id.employee_id.id)])

            faltas += self.ComputeDaysDiscount(initdate,enddate,contract_id)
            if payslips:
                for payslip in payslips:
                    neto = 0
                    for line in payslip.line_ids:
                        if line.code=='PGRAT':
                            acumulado += line.total

        salary = salary - (faltas * salary / 180 ) 
        print(salary)

        prov = (abs(salary) / 6 * months) - acumulado
        if contract_id.employee_id.affiliate_eps:
            prov = prov * (1+0.0675)
        else:
            prov = prov * (1+0.09)

        return prov