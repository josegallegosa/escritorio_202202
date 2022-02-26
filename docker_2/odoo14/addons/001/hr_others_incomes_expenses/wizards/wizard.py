# -*- coding: utf-8 -*-
from odoo import fields, models
import base64
from xlrd import open_workbook
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class HROthersIncomesExpensesWizard(models.TransientModel):
    _name = 'hr.others.incomes.expense.wizard'
    _description = 'Importador de Otros Ingresos/Egresos'

    import_file = fields.Binary(string='Archivo a importar')
    
    def import_files(self):
        if self.import_file:
            workbook = open_workbook(file_contents = base64.decodebytes(self.import_file))
            worksheet = workbook.sheet_by_index(0)
            l_verified = []

            d_line = {}
            for row in range(1,worksheet.nrows):
                if not self.env['hr.employee'].sudo().search([('identification_id','=',worksheet.cell(row,4).value)]):
                    raise ValidationError("No se encuentra el empleado con el número de documento: "+str(worksheet.cell(row,4).value))

                emp_id = self.env['hr.employee'].sudo().search([('identification_id','=',worksheet.cell(row,4).value)])
                contract_id = self.env['hr.contract'].search([('employee_id','=',emp_id.id),
                    ('state','=','open')], limit=1)

                if str(worksheet.cell(row,0).value) not in l_verified:
                    l_verified.append(str(worksheet.cell(row,0).value))
                    d_line[str(worksheet.cell(row,0).value)] = {
                        'name':worksheet.cell(row,1).value,
                        'input_type_id':self.env['hr.payslip.input.type'].search([('code','=',worksheet.cell(row,2).value)]).id,
                        'date':datetime.utcfromtimestamp((worksheet.cell(row,3).value - 25569) * 86400.0).strftime(DF),
                        'line_ids':[(0,0,{
                            'employee_id':self.env['hr.employee'].sudo().search([('identification_id','=',worksheet.cell(row,4).value)]).id,
                            'amount':worksheet.cell(row,6).value != '' and float(worksheet.cell(row,6).value) > 0 and (worksheet.cell(row,6).value/100)*contract_id.wage or worksheet.cell(row,5).value,
                            'percent':worksheet.cell(row,6).value})]
                    }
                else:
                    d_line[str(worksheet.cell(row,0).value)]['line_ids'].append((0,0,{
                        'employee_id':self.env['hr.employee'].sudo().search([('identification_id','=',worksheet.cell(row,4).value)]).id,
                            'amount':worksheet.cell(row,6).value != '' and float(worksheet.cell(row,6).value) > 0 and (worksheet.cell(row,6).value/100)*contract_id.wage or worksheet.cell(row,5).value,
                        'percent':worksheet.cell(row,6).value}))

            for line in l_verified:
                self.env['hr.others.incomes.expenses'].sudo().create(d_line[line])
