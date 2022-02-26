# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from datetime import datetime
import math

MONTH_SELECTION = [
    ('01', "ENERO"), ('02', "FEBRERO"), ('03', "MARZO"), ('04', "ABRIL"),
    ('05', "MAYO"), ('06', "JUNIO"), ('07', "JULIO"), ('08', "AGOSTO"),
    ('09', "SETIEMBRE"), ('10', "OCTUBRE"), ('11', "NOVIEMBRE"),
    ('12', "DICIEMBRE")]


def year_now():
    return datetime.now().year

YEAR_SELECTION = [(str(year), year) for year in range(2015, year_now()+3)]


def stryear(): return datetime.now().strftime('%Y')


def strmonth(): return datetime.now().strftime('%m')


class Hr5taParameterLine(models.Model):
    _name = 'hr.5ta.parameter.line'
    _description = 'Escalas de 5ta'
    _rec_name = 'sequence'
    _order = 'sequence'

    sequence = fields.Integer(string='Secuencia')
    init_value = fields.Integer(string='Valor inicial')
    final_value = fields.Integer(string='Valor final')
    percentage = fields.Float(string='Porcentaje')


class Hr5ta(models.Model):
    _name = 'hr.5ta'
    _description = 'Tabla de 5ta'

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True, index=True, readonly=True)
    month = fields.Selection(selection=MONTH_SELECTION, default=strmonth(), string='Mes')
    year = fields.Selection(selection=YEAR_SELECTION, default=stryear(), string='Año')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado')
    income_january = fields.Float(string='Ingresos Enero')
    income_february = fields.Float(string='Ingresos Febrero')
    income_march = fields.Float(string='Ingresos Marzo')
    income_april = fields.Float(string='Ingresos Abril')
    income_may = fields.Float(string='Ingresos Mayo')
    income_june = fields.Float(string='Ingresos Junio')
    income_july = fields.Float(string='Ingresos Julio')
    income_august = fields.Float(string='Ingresos Agosto')
    income_september = fields.Float(string='Ingresos Setiembre')
    income_october = fields.Float(string='Ingresos Octubre')
    income_november = fields.Float(string='Ingresos Noviembre')
    income_december = fields.Float(string='Ingresos Diciembre')
    income_to_date = fields.Float(string='Ingresos percibidos a la fecha',
                                             compute='get_income_to_date',store=True)
    income_projection_january = fields.Float(string='Proyección Enero')
    income_projection_february = fields.Float(string='Proyección Febrero')
    income_projection_march = fields.Float(string='Proyección Marzo')
    income_projection_april = fields.Float(string='Proyección Abril')
    income_projection_may = fields.Float(string='Proyección Mayo')
    income_projection_june = fields.Float(string='Proyección Junio')
    income_projection_july = fields.Float(string='Proyección Julio')
    income_projection_august = fields.Float(string='Proyección Agosto')
    income_projection_september = fields.Float(string='Proyección Setiembre')
    income_projection_october = fields.Float(string='Proyección Octubre')
    income_projection_november = fields.Float(string='Proyección Noviembre')
    income_projection_december = fields.Float(string='Proyección Diciembre')
    total_income_projection = fields.Float(string='Total Proyección',
        compute='get_total_income_projection',store=True)
    gratification_projection = fields.Float(string='Proyección de gratificación')
    amount_total = fields.Float(string='Ingreso Anual', compute='get_amount_total',store=True)
    accumulated_withholding = fields.Float(string='Retención acumulada')
    retention_of_the_month = fields.Float(string='Retención del mes')
    base_5ta = fields.Float(string='Base 5ta')
    annual_5ta = fields.Float(string='5ta Anual')


    def get_month(self, date_start):
        month = 13 - date_start.month
        print ('***********************************+',month)
        return month

    def get_data_last_month(self, employee, date):
        year = str(date.year)
        month = str(date.month-1).zfill(2)
        hr_5ta_id = self.search([('month', '=', month), ('year', '=', year), ('employee_id', '=', employee.id)])
        return hr_5ta_id

    def get_data_month(self, employee, date):
        year = str(date.year)
        month = str(date.month).zfill(2)
        hr_5ta_id = self.search([('month', '=', month), ('year', '=', year), ('employee_id', '=', employee.id)])
        return hr_5ta_id

    def get_data_month_values(self, employee, date):
        year = str(date.year)
        month = str(date.month-1).zfill(2)
        hr_5ta_id = self.search([('month', '=', month), ('year', '=', year), ('employee_id', '=', employee.id)])
        list_incomes=[]
        list_projections=[]
        if hr_5ta_id:
            list_incomes.extend([hr_5ta_id.income_january,hr_5ta_id.income_february,hr_5ta_id.income_march,hr_5ta_id.income_april,hr_5ta_id.income_may,hr_5ta_id.income_june,hr_5ta_id.income_july,hr_5ta_id.income_august,hr_5ta_id.income_september,hr_5ta_id.income_october,hr_5ta_id.income_november,hr_5ta_id.income_december])
            list_projections.extend([hr_5ta_id.income_projection_january,hr_5ta_id.income_projection_february,hr_5ta_id.income_projection_march,hr_5ta_id.income_projection_april,hr_5ta_id.income_projection_may,hr_5ta_id.income_projection_june,hr_5ta_id.income_projection_july,hr_5ta_id.income_projection_august,hr_5ta_id.income_projection_september,hr_5ta_id.income_projection_october,hr_5ta_id.income_projection_november,hr_5ta_id.income_projection_december])
        else:
            list_incomes.extend([0,0,0,0,0,0,0,0,0,0,0,0])
            list_projections.extend([0,0,0,0,0,0,0,0,0,0,0,0])
        return [list_incomes,list_projections]
            
    def get_scales_5ta(self,date):
        scales = self.env['hr.5ta.parameter.line'].search([],order='sequence')
        list_scales=[]
        uit = self.env['hr.payroll.parameters.line'].get_amount('UIT',  date)
        for scale in scales:
            dict_scale={}
            dict_scale['lower_limit'] = scale.init_value*uit
            dict_scale['upper_limit'] = scale.final_value*uit if scale.final_value>0 else math.inf
            dict_scale['percentage'] = scale.percentage
            list_scales.append(dict_scale)
        return list_scales

    def generate_data_5ta(self, contract, date, list_incomes, list_projections, gratification_projection,base_5ta,annual_5ta,accumulated_withholding,retention_of_the_month):
        hr_5ta_id = self.search([('month', '=', str(date.month).zfill(2)), ('year', '=', str(date.year)), ('employee_id', '=', contract.employee_id.id)])
        vals = {'year': str(date.year),
                'month': str(date.month).zfill(2),
                'employee_id': contract.employee_id.id,
                'income_january': list_incomes[0],
                'income_february': list_incomes[1],
                'income_march': list_incomes[2],
                'income_april': list_incomes[3],
                'income_may': list_incomes[4],
                'income_june': list_incomes[5],
                'income_july': list_incomes[6],
                'income_august': list_incomes[7],
                'income_september': list_incomes[8],
                'income_october': list_incomes[9],
                'income_november': list_incomes[10],
                'income_december': list_incomes[11],
                'income_projection_january': list_projections[0],
                'income_projection_february': list_projections[1],
                'income_projection_march': list_projections[2],
                'income_projection_april': list_projections[3],
                'income_projection_may': list_projections[4],
                'income_projection_june': list_projections[5],
                'income_projection_july': list_projections[6],
                'income_projection_august': list_projections[7],
                'income_projection_september': list_projections[8],
                'income_projection_october': list_projections[9],
                'income_projection_november': list_projections[10],
                'income_projection_december': list_projections[11],
                'gratification_projection': gratification_projection,
                'base_5ta': base_5ta,
                'annual_5ta': annual_5ta,
                'accumulated_withholding': accumulated_withholding,
                'retention_of_the_month': retention_of_the_month}
        if not hr_5ta_id:
            self.create(vals)

    @api.depends('income_january', 'income_february', 'income_march', 'income_april',
                 'income_may', 'income_june', 'income_july', 'income_august',
                 'income_september', 'income_october', 'income_november', 'income_december')
    def get_income_to_date(self):
        self.ensure_one()
        self.income_to_date = self.income_january + self.income_february + self.income_march+ self.income_april + self.income_may + self.income_june + self.income_july + self.income_august + self.income_september + self.income_october + self.income_november + self.income_december


    @api.depends('income_projection_january', 'income_projection_february', 'income_projection_march', 'income_projection_april',
                 'income_projection_may', 'income_projection_june', 'income_projection_july', 'income_projection_august',
                 'income_projection_september', 'income_projection_october', 'income_projection_november', 'income_projection_december')
    def get_total_income_projection(self):
        self.ensure_one()
        self.total_income_projection = self.income_projection_january + self.income_projection_february + self.income_projection_march+ self.income_projection_april + self.income_projection_may + self.income_projection_june + self.income_projection_july + self.income_projection_august + self.income_projection_september + self.income_projection_october + self.income_projection_november + self.income_projection_december

    @api.depends('income_to_date','total_income_projection','gratification_projection')
    def get_amount_total(self):
        self.ensure_one()
        self.amount_total = self.income_to_date+self.total_income_projection+self.gratification_projection

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    def _compute_rule(self, localdict):
        self.ensure_one()
        localdict['quinta_obj'] = self.env['hr.5ta']
        return super(HrSalaryRule,self)._compute_rule(localdict)

    def _satisfy_condition(self, localdict):
        self.ensure_one()
        localdict['quinta_obj'] = self.env['hr.5ta']
        return super(HrSalaryRule, self)._satisfy_condition(localdict)
