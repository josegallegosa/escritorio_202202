# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from odoo.exceptions import UserError
import datetime
import math

class HRRecalculationPr2(models.Model):
    _name = 'hr.recalculation.pr2'
    _description = 'Recálculo PR2'

    name = fields.Char(string='Nombre Recálculo PR2')

    base_period = fields.Selection(
        string="Periodo Base",
        selection=[
            ('per1', 'Diciembre año anterior a noviembre año actual'),
            ('per2', 'Junio año anterior a mayo año actual'),
        ], default="per1"
    )   

    current_date = fields.Date(default=fields.Date.context_today, string='Fecha Actual')


    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True, index=True, readonly=True)

    recalculation_pr2_ids = fields.One2many(comodel_name='hr.recalculation.pr2.line',inverse_name='recalculation_pr2_id',string='Recálculo PR2')

    @api.model
    def create_details(self, pr2):
        employees = self.env['hr.employee'].search([('company_id', '=', self.env.company.id)])
        print(self.env.company.id)

        current_date = pr2.current_date
        for employee in employees:
            if pr2.base_period == 'per1':
                print("Entro if per1")
                contract_ids = employee._get_contracts(datetime.datetime(current_date.year-1, 12, 1), datetime.datetime(current_date.year, 11, 30))
            else:
                print("Entro if per2")
                contract_ids = employee._get_contracts(datetime.datetime(current_date.year-1, 6, 1), datetime.datetime(current_date.year, 5, 31))
            if contract_ids:
                val = {
                    'employee_id': employee.id,
                    'recalculation_pr2_id': pr2.id,
                    
                    #'country_id': employee.company_id.country_id.id
                }

                for key, value in val.items():
                    print (key, 'value', value)
                print(val)
                
                if contract_ids.state == 'open': 
                    if contract_ids.date_end==False:
                        self.env['hr.recalculation.pr2.line'].create(val)
                    elif contract_ids.date_end > current_date:
                        self.env['hr.recalculation.pr2.line'].create(val)
        return True

    @api.model
    def create(self, vals):
        my_id = super(HRRecalculationPr2, self).create(vals)
        self.create_details(my_id)
        return my_id

class HRRecalculationPr2Line(models.Model):
    _name = 'hr.recalculation.pr2.line'
    _description = 'Recálculo PR2 Línea'

    _rec_name = 'employee_id'

    recalculation_pr2_id = fields.Many2one(comodel_name='hr.recalculation.pr2',string='Recálculo PR2')

    employee_id = fields.Many2one(comodel_name='hr.employee',string='Empleado')
    monthly_labor_income = fields.Float(compute='_method_recalculation_pr2',string='Ingreso Laboral Mensual')
    monthly_average = fields.Float(compute='_method_recalculation_pr2',sting='Promedio Mensual')
    monthly_average_uvt = fields.Float(compute='_method_recalculation_pr2',string='Promedio Mensual en UVT')
    value_according_to_table = fields.Float(compute='_method_recalculation_pr2',string='Valor Según Tabla')
    percentage_process_two = fields.Float(compute='_method_recalculation_pr2',string='% Procedimiento 2')

    contract_id = fields.Many2one(comodel_name='hr.contract',string='Contrato')

    
    @api.depends('employee_id', 'recalculation_pr2_id')
    def _method_recalculation_pr2(self):
        for linea in self:

            var_current_date = datetime.datetime(linea.recalculation_pr2_id.current_date.year,linea.recalculation_pr2_id.current_date.month,1)

            var_base_period = linea.recalculation_pr2_id.base_period 
            date_from = datetime.datetime(var_current_date.year, var_current_date.month, 1)


            if var_base_period == 'per1':
                
                limit_inf_date_from = datetime.datetime(var_current_date.year-1, 12, 1)
                limit_sup_date_from = datetime.datetime(var_current_date.year, 11, 30) 
                if limit_sup_date_from > var_current_date:
                    limit_sup_date_from = var_current_date

                contract_ids = linea.employee_id._get_contracts(limit_inf_date_from, limit_sup_date_from)
                
                type_struct_id = contract_ids.structure_type_id.id
                struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

                payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',limit_inf_date_from),('date_from','<',limit_sup_date_from),('struct_id','=',struct_id.id),
                ('employee_id', '=', linea.employee_id.id)], order="date_from")
            else:

                limit_inf_date_from = datetime.datetime(var_current_date.year-1, 6, 1)
                limit_sup_date_from = datetime.datetime(var_current_date.year, 5, 31)
                if limit_sup_date_from > var_current_date:
                    limit_sup_date_from = var_current_date

                contract_ids = linea.employee_id._get_contracts(limit_inf_date_from, limit_sup_date_from)
            
                type_struct_id = contract_ids.structure_type_id.id
                struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id)],limit=1)

                payslips = self.env['hr.payslip'].sudo().search([('date_from','>=',limit_inf_date_from),('date_from','<',limit_sup_date_from),('struct_id','=',struct_id.id),
                ('employee_id', '=', linea.employee_id.id)], order="date_from")


            suma = 0

            if payslips:
                for payslip in payslips:
                    for line in payslip.line_ids:
                        if line.category_id.code=='ILMR':
                            suma += line.total

                linea.monthly_labor_income = suma
            
            else:
                linea.monthly_labor_income = 0

            if len(payslips)==0:
                linea.monthly_average = 0
            else:
                linea.monthly_average = suma/len(payslips)

            uvt = self.env['hr.payroll.parameters.line'].get_amount('UVT',  date_from)

            linea.monthly_average_uvt = linea.monthly_average/uvt    

            linea.value_according_to_table = self.env['hr.employee'].GetRetentionAtTheSource(date_from,linea.monthly_average_uvt)/uvt                

            
            if len(payslips)==0:
                linea.percentage_process_two = 0
            else:
                linea.percentage_process_two = linea.value_according_to_table/linea.monthly_average_uvt





    
