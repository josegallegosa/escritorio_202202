# -*- coding: utf-8 -*-

from odoo import fields, models
import base64
import requests
from xlrd import open_workbook
import os
import re
import unicodedata

class TxtWizardExport(models.TransientModel):
    _name = 'txt.wizard.export'
    _description = 'Descargar txt nominas'

    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)

    partner_id = fields.Many2one('res.partner', string='Company',related='company_id.partner_id')

    acount_bank_company_id = fields.Many2one(comodel_name='res.partner.bank',string='Cuenta de Banco Compañia')
    

    period_id = fields.Many2one('hr.payroll.period', 'Periodo')
    
    current_date = fields.Date(default=fields.Date.context_today, string='Fecha Actual')
    
    year = fields.Char(compute='get_year', string='Año')
    month = fields.Char(compute='get_month', string='Mes')
    ruc = fields.Char(compute='get_ruc', string='RUC')

    def get_year(self):
        for line in self:
            line.year = line.period_id.date_start.year

    def get_month(self):
        for line in self:
            line.month = line.period_id.date_start.month

    def get_ruc(self):
        for line in self:
            line.ruc = self.env['res.users'].search([('id', '=', line._context.get('uid'))]).company_id.partner_id.vat

    def convert_str(self, s):
        return s and str(s) or ' '

    def white_spaces(self,cad,cant,pos,char):
        space = ''
        for i in range(cant-len(str(cad))):
            space +=char
        if pos == 'right':
            union = str(cad)+space 
            return union[0:cant]
        if pos == 'left':
            union = space+str(cad)
            return union[len(union)-cant:len(union)]
    
    def type_account_company(self, field):
        if field == '37':
            return 'S'
        elif field == '27':
            return 'D'
        else: 
            return field
    def validation_identification_employee(self, validation,field):
        if validation == 'passport':
            return '5'+str(field)
        else:    
            return str(field)

    def delete_tildes(self,cadena):

      s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
      return s
    
    def method_exporter_txt(self):

        RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
        payslip_run_id = self.env['hr.payslip.run'].browse(self.env.context.get('active_id', False))
        sequence = 1

        current_date = fields.Datetime.context_timestamp(self,fields.Datetime.now())
        
        res = []
        lines_control_register = {}
        lines_detail_register = {}
        lines_final_register = {}

        nap = 0
        total = 0
                
        #BANCO - BANCO AV VILLAS
        if self.acount_bank_company_id.bank_id.code == '52':
            

            type_of_register_control = '01'  
            date = self.current_date.strftime("%Y%m%d")
            hour = current_date.strftime("%H%M%S")
            code_office = '088'
            code_acquirer = '02'
            filename = self.white_spaces('',50,'right',' ')
            stuffed_control = self.white_spaces('',120,'right',' ')

            lines_control_register[1] = [
                          self.convert_str(type_of_register_control),
                          self.convert_str(date),
                          self.convert_str(hour),
                          self.convert_str(code_office),
                          self.convert_str(code_acquirer),
                          self.convert_str(filename),
                          self.convert_str(stuffed_control),
                          ]
            #VALIDACIÓN
            print("linea inicial")
            pos_i = 1
            pos_f = 1
            for i in lines_control_register[1]:
                pos_f = pos_i + len(i) -1
                print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                pos_i = pos_f+1


            for x in lines_control_register:
                elements = [
                    lines_control_register[x][0],
                    lines_control_register[x][1],
                    lines_control_register[x][2],
                    lines_control_register[x][3],
                    lines_control_register[x][4],
                    lines_control_register[x][5],
                    lines_control_register[x][6],
                ]
                res.append(''.join(elements))


            
            

            for payslips in payslip_run_id:
                for payslip in payslips.slip_ids:
                    for line in payslip.line_ids:
                            if line.category_id.code=='NAP':
                                nap += line.total
                                total += line.total
                    type_of_register_detail = '02'
                    code_transaction = '000023'
                    type_product_origin = self.white_spaces(self.acount_bank_company_id.acc_type_bank.code,2,'left','0')
                    number_root_account = self.white_spaces(self.acount_bank_company_id.acc_number,16,'left','0')
                    destination_entity = self.white_spaces(payslip.employee_id.account_bank_principal.bank_id.code,3,'left','0')
                    type_destination_product = self.white_spaces(payslip.employee_id.account_bank_principal.acc_type_bank.code,2,'left','0')
                    number_destination_account = self.white_spaces(payslip.employee_id.account_bank_principal.acc_number,16,'left','0')
                    number_sequence = self.white_spaces(sequence,9,'left','0')
                    value_to_transfer = self.white_spaces(int(round(nap,0)),18,'left','0')
                    number_bill = self.white_spaces('',16,'left','0')
                    reference_1 = self.white_spaces('',16,'left','0')
                    reference_2 = self.white_spaces('',16,'left','0')
                    name = self.white_spaces(str(payslip.employee_id.name)+' '+str(payslip.employee_id.last_name)+' '+str(payslip.employee_id.mother_last_name),30,'right',' ')
                    number_document = self.white_spaces(payslip.employee_id.identification_id,11,'left','0')
                    number_authorization = self.white_spaces('',6,'left','0')
                    code_response = self.white_spaces('',2,'left','0')
                    contigent_hold = self.white_spaces('',18,'left','0')
                    stuffed_detail = self.white_spaces('',2,'left','0')


                    
                    code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
                    
                    lines_detail_register[code] = [
                          self.convert_str(type_of_register_detail),
                          self.convert_str(code_transaction),
                          self.convert_str(type_product_origin),
                          self.convert_str(number_root_account),
                          self.convert_str(destination_entity),
                          self.convert_str(type_destination_product),
                          self.convert_str(number_destination_account),
                          self.convert_str(number_sequence),
                          self.convert_str(value_to_transfer),
                          self.convert_str(number_bill),
                          self.convert_str(reference_1),
                          self.convert_str(reference_2),
                          self.convert_str(name),
                          self.convert_str(number_document),
                          self.convert_str(number_authorization),
                          self.convert_str(code_response),
                          self.convert_str(contigent_hold),
                          self.convert_str(stuffed_detail),
                          ]
                    #VALIDACIÓN
                    print("lineas nominas")
                    pos_i = 1
                    pos_f = 1
                    for i in lines_detail_register[code]:
                        pos_f = pos_i + len(i) -1
                        print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                        pos_i = pos_f+1


                    sequence += 1
                    nap = 0
            sequence = 0

            for x in lines_detail_register:
                elements = [
                    lines_detail_register[x][0],
                    lines_detail_register[x][1],
                    lines_detail_register[x][2],
                    lines_detail_register[x][3],
                    lines_detail_register[x][4],
                    lines_detail_register[x][5],
                    lines_detail_register[x][6],
                    lines_detail_register[x][7],
                    lines_detail_register[x][8],
                    lines_detail_register[x][9],
                    lines_detail_register[x][10],
                    lines_detail_register[x][11],
                    lines_detail_register[x][12],
                    lines_detail_register[x][13],
                    lines_detail_register[x][14],
                    lines_detail_register[x][15],
                    lines_detail_register[x][16],
                    lines_detail_register[x][17],
                ]
                res.append(''.join(elements))

            type_of_register_final = '03'
            total_amount_of_records_detail = self.white_spaces(len(payslips.slip_ids),9,'left','0')
            total_transactions_value = self.white_spaces(int(round(total,0)),20,'left','0')
            check_digit = self.white_spaces('',15,'left',' ')
            stuffed_final = self.white_spaces('',145,'left','0')

            

            lines_final_register[2] = [
                          self.convert_str(type_of_register_final),
                          self.convert_str(total_amount_of_records_detail),
                          self.convert_str(total_transactions_value),
                          self.convert_str(check_digit),
                          self.convert_str(stuffed_final),
                          ]
            #VALIDACIÓN
            print("lineas finales")
            pos_i = 1
            pos_f = 1
            for i in lines_final_register[2]:
                pos_f = pos_i + len(i) -1
                print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                pos_i = pos_f+1

            for x in lines_final_register:
                elements = [
                    lines_final_register[x][0],
                    lines_final_register[x][1],
                    lines_final_register[x][2],
                    lines_final_register[x][3],
                    lines_final_register[x][4],
                ]
                res.append(''.join(elements))


        #BANCO - BancolombiaACH
        elif self.acount_bank_company_id.bank_id.name == 'BANCOLOMBIA S.A. ACH':   

            for payslips in payslip_run_id:
                for payslip in payslips.slip_ids:
                    for line in payslip.line_ids:
                            if line.category_id.code=='NAP':
                                total += line.total

            type_of_register_control = '1'
            nit_company = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.vat,10,'left','0')
            business_name = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.name,16,'right',' ')
            transaction = '225'
            description = self.white_spaces('PagoNómina',10,'left',' ')
            date_mvto = self.current_date.strftime("%Y%m%d")[2:4]+self.current_date.strftime("%Y%m%d")[4:8]
            sequence = 'A'
            date_payment = self.current_date.strftime("%Y%m%d")[2:4]+self.current_date.strftime("%Y%m%d")[4:8]
            total_records = self.white_spaces(len(payslip_run_id.slip_ids),6,'left','0')
            debit_value = self.white_spaces(int(round(total,0)),12,'left','0')
            credit_value = self.white_spaces('',12,'left','0')
            bank_account = self.white_spaces(self.acount_bank_company_id.acc_number,11,'left','0')
            account_type = self.white_spaces(self.type_account_company(self.acount_bank_company_id.acc_type_bank.code),1,'left',' ')

            lines_control_register[1] = [
                          self.convert_str(type_of_register_control),
                          self.convert_str(nit_company),
                          self.convert_str(business_name),
                          self.convert_str(transaction),
                          self.convert_str(description),
                          self.convert_str(date_mvto),
                          self.convert_str(sequence),
                          self.convert_str(date_payment),
                          self.convert_str(total_records),
                          self.convert_str(debit_value),
                          self.convert_str(credit_value),
                          self.convert_str(bank_account),
                          self.convert_str(account_type),
                          ]
            #VALIDACIÓN
            print("linea inicial")
            pos_i = 1
            pos_f = 1
            for i in lines_control_register[1]:
                pos_f = pos_i + len(i) -1
                print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                pos_i = pos_f+1

            for x in lines_control_register:
                elements = [
                    lines_control_register[x][0],
                    lines_control_register[x][1],
                    lines_control_register[x][2],
                    lines_control_register[x][3],
                    lines_control_register[x][4],
                    lines_control_register[x][5],
                    lines_control_register[x][6],
                    lines_control_register[x][7],
                    lines_control_register[x][8],
                    lines_control_register[x][9],
                    lines_control_register[x][10],
                    lines_control_register[x][11],
                    lines_control_register[x][12],
                ]
                res.append(''.join(elements))


            sequence = 1


            

            for payslips in payslip_run_id:
                for payslip in payslips.slip_ids:
                    for line in payslip.line_ids:
                            if line.category_id.code=='NAP':
                                nap += line.total
                                total += line.total
                    type_of_register_detail = '6'
                    employee_identification = self.white_spaces(payslip.employee_id.identification_id,15,'left','0')
                    name_employee = self.white_spaces(str(payslip.employee_id.name)+' '+str(payslip.employee_id.last_name)+' '+str(payslip.employee_id.mother_last_name),18,'right',' ')
                    payment_site = self.white_spaces('',9,'right',' ')
                    acccount_number = self.white_spaces(payslip.employee_id.account_bank_principal.acc_number,17,'left','0')
                    transaction_place = 'S'
                    account_type = self.white_spaces(payslip.employee_id.account_bank_principal.acc_type_bank.code,2,'left','0')
                    scattered_value = self.white_spaces(int(round(nap,0)),10,'left','0')
                    payment_concept = self.white_spaces(payslip_run_id.name,9,'left','0')
                    transaction_reference = self.white_spaces('',16,'left','0')
                    whites = self.white_spaces('',16,'left','0')
                    

                    
                    code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
                    
                    lines_detail_register[code] = [
                          self.convert_str(type_of_register_detail),
                          self.convert_str(employee_identification),
                          self.convert_str(name_employee),
                          self.convert_str(payment_site),
                          self.convert_str(acccount_number),
                          self.convert_str(transaction_place),
                          self.convert_str(account_type),
                          self.convert_str(scattered_value),
                          self.convert_str(payment_concept),
                          self.convert_str(transaction_reference),
                          self.convert_str(whites),
                          ]
                    #VALIDACIÓN
                    print("lineas nominas")
                    pos_i = 1
                    pos_f = 1
                    for i in lines_detail_register[code]:
                        pos_f = pos_i + len(i) -1
                        print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                        pos_i = pos_f+1

                    sequence += 1
                    nap = 0
                sequence = 0

            for x in lines_detail_register:
                elements = [
                    lines_detail_register[x][0],
                    lines_detail_register[x][1],
                    lines_detail_register[x][2],
                    lines_detail_register[x][3],
                    lines_detail_register[x][4],
                    lines_detail_register[x][5],
                    lines_detail_register[x][6],
                    lines_detail_register[x][7],
                    lines_detail_register[x][8],
                    lines_detail_register[x][9],
                    lines_detail_register[x][10],
                ]
                res.append(''.join(elements))


        #BANCO - BancolombiaPAB
        elif self.acount_bank_company_id.bank_id.name == 'BANCOLOMBIA S.A. PAB':
            

            type_of_register_control = '1'
            nit_company = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.vat,15,'left','0')
            application = 'I'
            business_name = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.name,15,'right',' ')
            transaction = '225'
            description = self.white_spaces('PagoNómina',10,'left',' ')
            date_mvto = self.current_date.strftime("%Y%m%d")
            sequence = self.white_spaces('A',2,'left',' ')
            date_payment = self.current_date.strftime("%Y%m%d")
            total_records = self.white_spaces(len(payslip_run_id.slip_ids),6,'left','0')
            debit_value = self.white_spaces(int(round(total,0)),17,'left','0')
            credit_value = self.white_spaces('',17,'left','0')
            bank_account = self.white_spaces(self.acount_bank_company_id.acc_number,11,'left','0')
            account_type = self.white_spaces(self.type_account_company(self.acount_bank_company_id.acc_type_bank.code),1,'left',' ')
            whites = self.white_spaces('',149,'left','0')
            
            lines_control_register[1] = [
                          self.convert_str(type_of_register_control),
                          self.convert_str(nit_company),
                          self.convert_str(application),
                          self.convert_str(business_name),
                          self.convert_str(transaction),
                          self.convert_str(description),
                          self.convert_str(date_mvto),
                          self.convert_str(sequence),
                          self.convert_str(date_payment),
                          self.convert_str(total_records),
                          self.convert_str(debit_value),
                          self.convert_str(credit_value),
                          self.convert_str(bank_account),
                          self.convert_str(account_type),
                          self.convert_str(whites),
                          ]
            #VALIDACIÓN
            print("linea inicial")
            pos_i = 1
            pos_f = 1
            for i in lines_control_register[1]:
                pos_f = pos_i + len(i) -1
                print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                pos_i = pos_f+1

            for x in lines_control_register:
                elements = [
                    lines_control_register[x][0],
                    lines_control_register[x][1],
                    lines_control_register[x][2],
                    lines_control_register[x][3],
                    lines_control_register[x][4],
                    lines_control_register[x][5],
                    lines_control_register[x][6],
                    lines_control_register[x][7],
                    lines_control_register[x][8],
                    lines_control_register[x][9],
                    lines_control_register[x][10],
                    lines_control_register[x][11],
                    lines_control_register[x][12],
                ]
                res.append(''.join(elements))


            sequence = 1

            
            

            for payslips in payslip_run_id:
                for payslip in payslips.slip_ids:
                    for line in payslip.line_ids:
                            if line.category_id.code=='NAP':
                                nap += line.total
                                total += line.total
                    type_of_register_detail = '6'
                    employee_identification = self.white_spaces(self.validation_identification_employee(payslip.employee_id.type_document_id.l10n_co_document_code,payslip.employee_id.identification_id),15,'left','0')
                    name_employee = self.white_spaces(str(payslip.employee_id.name)+' '+str(payslip.employee_id.last_name)+' '+str(payslip.employee_id.mother_last_name),30,'right',' ')
                    payment_site = self.white_spaces('',9,'right',' ')
                    acccount_number = self.white_spaces(payslip.employee_id.account_bank_principal.acc_number,17,'left','0')
                    transaction_place = 'S'
                    account_type = self.white_spaces(payslip.employee_id.account_bank_principal.acc_type_bank.code,2,'left','0')
                    scattered_value = self.white_spaces(int(round(nap,0)),17,'left','0')
                    date_application = self.current_date.strftime("%Y%m%d")
                    transaction_reference = self.white_spaces('',21,'left','0')
                    whites = self.white_spaces('',143,'left','0')

                    
                    code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
                    
                    lines_detail_register[code] = [
                          self.convert_str(type_of_register_detail),
                          self.convert_str(employee_identification),
                          self.convert_str(name_employee),
                          self.convert_str(payment_site),
                          self.convert_str(acccount_number),
                          self.convert_str(transaction_place),
                          self.convert_str(account_type),
                          self.convert_str(scattered_value),
                          self.convert_str(date_application),
                          self.convert_str(transaction_reference),
                          self.convert_str(whites),
                          ]
                    #VALIDACIÓN
                    print("lineas nominas")
                    pos_i = 1
                    pos_f = 1
                    for i in lines_detail_register[code]:
                        pos_f = pos_i + len(i) -1
                        print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                        pos_i = pos_f+1


                    sequence += 1
                    nap = 0
                sequence = 0

            for x in lines_detail_register:
                elements = [
                    lines_detail_register[x][0],
                    lines_detail_register[x][1],
                    lines_detail_register[x][2],
                    lines_detail_register[x][3],
                    lines_detail_register[x][4],
                    lines_detail_register[x][5],
                    lines_detail_register[x][6],
                    lines_detail_register[x][7],
                    lines_detail_register[x][8],
                    lines_detail_register[x][9],
                    lines_detail_register[x][10],
                ]
                res.append(''.join(elements))

        #BANCO - COLPATRIA
        elif self.acount_bank_company_id.bank_id.code == '19':
            

            type_of_register_control = '1'
            nit_company = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.vat,15,'left','0')
            application = 'I'
            business_name = self.white_spaces(self.acount_bank_company_id.company_id.partner_id.name,15,'right',' ')
            transaction = '225'
            description = self.white_spaces('PagoNómina',10,'left',' ')
            date_mvto = self.current_date.strftime("%Y%m%d")
            sequence = self.white_spaces('A',2,'left',' ')
            date_payment = self.current_date.strftime("%Y%m%d")
            total_records = self.white_spaces(len(payslip_run_id.slip_ids),6,'left','0')
            debit_value = self.white_spaces(int(round(total,0)),17,'left','0')
            credit_value = self.white_spaces('',17,'left','0')
            bank_account = self.white_spaces(self.acount_bank_company_id.acc_number,11,'left','0')
            account_type = self.white_spaces(self.type_account_company(self.acount_bank_company_id.acc_type_bank.code),1,'left',' ')
            whites = self.white_spaces('',149,'left','0')
            
            lines_control_register[1] = [
                          self.convert_str(type_of_register_control),
                          self.convert_str(nit_company),
                          self.convert_str(application),
                          self.convert_str(business_name),
                          self.convert_str(transaction),
                          self.convert_str(description),
                          self.convert_str(date_mvto),
                          self.convert_str(sequence),
                          self.convert_str(date_payment),
                          self.convert_str(total_records),
                          self.convert_str(debit_value),
                          self.convert_str(credit_value),
                          self.convert_str(bank_account),
                          self.convert_str(account_type),
                          self.convert_str(whites),
                          ]
            #VALIDACIÓN
            print("linea inicial")
            pos_i = 1
            pos_f = 1
            for i in lines_control_register[1]:
                pos_f = pos_i + len(i) -1
                print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                pos_i = pos_f+1

            for x in lines_control_register:
                elements = [
                    lines_control_register[x][0],
                    lines_control_register[x][1],
                    lines_control_register[x][2],
                    lines_control_register[x][3],
                    lines_control_register[x][4],
                    lines_control_register[x][5],
                    lines_control_register[x][6],
                    lines_control_register[x][7],
                    lines_control_register[x][8],
                    lines_control_register[x][9],
                    lines_control_register[x][10],
                    lines_control_register[x][11],
                    lines_control_register[x][12],
                ]
                res.append(''.join(elements))


            sequence = 1

            
            

            for payslips in payslip_run_id:
                for payslip in payslips.slip_ids:
                    for line in payslip.line_ids:
                            if line.category_id.code=='NAP':
                                nap += line.total
                                total += line.total
                    type_of_register_detail = '6'
                    employee_identification = self.white_spaces(self.validation_identification_employee(payslip.employee_id.type_document_id.l10n_co_document_code,payslip.employee_id.identification_id),15,'left','0')
                    name_employee = self.white_spaces(payslip.employee_id.name+' '+payslip.employee_id.last_name+' '+payslip.employee_id.mother_last_name,30,'right',' ')
                    payment_site = self.white_spaces('',9,'right',' ')
                    acccount_number = self.white_spaces(payslip.employee_id.account_bank_principal.acc_number,17,'left','0')
                    transaction_place = 'S'
                    account_type = self.white_spaces(payslip.employee_id.account_bank_principal.acc_type_bank.code,2,'left','0')
                    scattered_value = self.white_spaces(int(round(nap,0)),17,'left','0')
                    date_application = self.current_date.strftime("%Y%m%d")
                    transaction_reference = self.white_spaces('',21,'left','0')
                    whites = self.white_spaces('',143,'left','0')

                    
                    code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
                    
                    lines_detail_register[code] = [
                          self.convert_str(type_of_register_detail),
                          self.convert_str(employee_identification),
                          self.convert_str(name_employee),
                          self.convert_str(payment_site),
                          self.convert_str(acccount_number),
                          self.convert_str(transaction_place),
                          self.convert_str(account_type),
                          self.convert_str(scattered_value),
                          self.convert_str(date_application),
                          self.convert_str(transaction_reference),
                          self.convert_str(whites),
                          ]
                    #VALIDACIÓN
                    print("lineas nominas")
                    pos_i = 1
                    pos_f = 1
                    for i in lines_detail_register[code]:
                        pos_f = pos_i + len(i) -1
                        print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                        pos_i = pos_f+1


                    sequence += 1
                    nap = 0
                sequence = 0

            for x in lines_detail_register:
                elements = [
                    lines_detail_register[x][0],
                    lines_detail_register[x][1],
                    lines_detail_register[x][2],
                    lines_detail_register[x][3],
                    lines_detail_register[x][4],
                    lines_detail_register[x][5],
                    lines_detail_register[x][6],
                    lines_detail_register[x][7],
                    lines_detail_register[x][8],
                    lines_detail_register[x][9],
                    lines_detail_register[x][10],
                ]
                res.append(''.join(elements))

        else:
            res.append('NO HAY PLANTILLA PARA EL BANCO: '+str(self.acount_bank_company_id.bank_id.name))
            

        name = 'Exportado.txt'

        with open(RUTA_BASE+"/../static/src/archivos/"+name, 'w') as f:
            for item in res:
                f.write("%s\n" % self.delete_tildes(item))
            f.close()


        return {
        'name': "Exportado txt banco",
        'type': 'ir.actions.act_url',
        'url': self.env['ir.config_parameter'].get_param('web.base.url')+'/hr_export_txt/static/src/archivos/'+name,
        'target': 'new',
        }
        

