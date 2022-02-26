# -*- coding: utf-8 -*-
##############################################################################
from odoo import api, models, fields
import base64
import requests
from xlrd import open_workbook
import os
import re
import unicodedata

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    is_vacation = fields.Boolean(string='Vacaciones')

    VALUES = [
        ('sln', 'Suspensión temporal del contrato de trabajo o Comisión de servicios'),
        ('ige', 'Incapacidad EPS'),
        ('irl', 'Incapacidad por accidente de trabajo o Enfermedad laboral'),
        ('lma', 'Licencia de Maternidad'),
        ('lpa', 'Licencia de Paternidad'),
        ('vco', 'Vacaciones Compensadas'),
        ('vdi', 'Vacaciones Disfrutadas'),
        ('vre', 'Vacaciones por Retiro'),
        ('lr', 'Licencia remunerada'),
        ('lnr', 'Licencia no Remunerada'),
        ('lt', 'Licencia de Luto'),

    ]
    novelty = fields.Selection(
      string="Tipo de Ausencia",
      selection=VALUES,
      
    ) 

class PlameFileSave(models.TransientModel):
    _name = 'plame.file.save'

    output_name_14 = fields.Char('Output filename', size=128)
    output_file_14 = fields.Binary('Output file', readonly=True, filename="output_name_14")
    output_name_18 = fields.Char('Output filename', size=128)
    output_file_18 = fields.Binary('Output file', readonly=True, filename="output_name_18")


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    plame_id = fields.Many2one(comodel_name='hr.plame', string='Plame')

class HRPlame(models.Model):
    _name = 'hr.plame'

    name = fields.Char('Nombre')
    period_id = fields.Many2one('hr.payroll.period', 'Periodo')
    payslip_run_id = fields.One2many(comodel_name='hr.payslip.run',
                                     inverse_name='plame_id',
                                     string="Nóminas")
    year = fields.Char(compute='get_year', string='Año')
    month = fields.Char(compute='get_month', string='Mes')
    ruc = fields.Char(compute='get_ruc', string='RUC')

    @api.onchange('period_id')
    def onchange_period_id_lotes(self):

      payslip_run_id = self.env['hr.payslip.run'].search([('period_id','=',self.period_id.id)])
      self.payslip_run_id = payslip_run_id.ids


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

    def convert_amount(self, a):
        return a and str(a) or ''

    def get_hours(self, f):
        return int(f) or 0

    def get_minutes(self, f):
        return (abs(f) - abs(int(f)))*60/10 or 0

    current_date = fields.Date(default=fields.Date.context_today, string='Fecha Actual')

    company_id = fields.Many2one('res.company', string='Company',default=lambda self: self.env.company)

    def convert_str(self, s):
        return s and str(s) or ' '

    def white_spaces(self,cad,cant,pos,char):
        space = ''
        if cad == False:
          cad = ''
        for i in range(cant-len(str(cad))):
            space +=char
        if pos == 'right':
            union = str(cad)+space 
            return union[0:cant]
        if pos == 'left':
            union = space+str(cad)
            return union[len(union)-cant:len(union)]

    def delete_tildes(self,cadena):

      s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
      return s

    def validate_boolean(self, field):
      if field == False:
        return ' '
      else:
        return 'X'
        
    def first_substring(self, field):
      field = str(field)
      pf = 0
      for i in field:
        if i == ' ':
          break
        pf += 1
 
      return field[0:pf]

    def second_substring(self, field):
      field = str(field)
      pi = len(self.first_substring(field)) + 1

      pf = 0
      cont = 1
      for i in field:
        if i == ' ' and cont == 2:
          cont += 1
          break
        pf += 1
           
      return field[pi:pf]

    def entry_employee(self, date_start_contract, date_from_payslip ):
      if date_start_contract.strftime("%Y%m") == date_from_payslip.strftime("%Y%m"):
        return 'X'
      else:
        return ' '

    def exit_employee(self, date_end_contract, date_to_payslip ):
      if date_end_contract == False:
        return ' '
      elif date_end_contract.strftime("%Y%m") == date_to_payslip.strftime("%Y%m"):
        return 'X'
      else:
        return ' '
    def is_integral_salary(self, field):
      struct_id_s_t = self.env.ref('hr_payroll_rg_co.structure_s_i_co').id
      if field == struct_id_s_t:
        return 'X'
      else:
        return ' '

    def health_contribution_rate(self, salary, date):      
      smmlv = self.env['hr.payroll.parameters.line'].get_amount('SMMLV',  date)

      if  salary > 10*smmlv:
        return '0.125'
      else:
        return '0.04'

    def condition_senp(self, total_category_dss, date):      
      smmlv = self.env['hr.payroll.parameters.line'].get_amount('SMMLV',  date)

      if  total_category_dss > 10*smmlv:
        return '0.02'
      else:
        return '0.0'

    def condition_icbp(self, total_category_dss, date):      
      smmlv = self.env['hr.payroll.parameters.line'].get_amount('SMMLV',  date)

      if  total_category_dss > 10*smmlv:
        return '0.03'
      else:
        return '0.0'

    def contributing_condition_exonerated(self, total_ibcs, date):
      smmlv = self.env['hr.payroll.parameters.line'].get_amount('SMMLV',  date)

      if  total_ibcs > 10*smmlv:
        return 'N'
      else:
        return 'S'
    def pension_special_rate_indicator(self, field):
      if field == 'Pension' or field == 'Copiloto':
        return '4'
      else:
        return ''

    def ibc_other_parafiscals_other_than_ccf(self, condition, field):
      if condition == 'N':
        return int(round(field,2))
      else:
        return '0'

    def value_rule(self, field, code):
      const = 0
      for line in field:
        if line.code == code:
            const += line.total
      return const

    def value_category_rule(self, field, code):
      const = 0
      for line in field:
        if line.category_id.code == code:
            const += line.total
      return const

    def validate_novelty_sln(self, field):
      if field > 0:
        return True
      else:
        return False


    def date_entry(self, condition, date_entry_contract_employee):
      if condition == 'X':
        return date_entry_contract_employee.strftime("%Y-%m-%d")
      else:
        return ''

    def date_exit(self, condition, date_exit_contract_employee):
      if condition == 'X':
        return date_exit_contract_employee.strftime("%Y-%m-%d")
      else:
        return ''

    def permanent_variation_of_salary(self, type_struct_id_employee, date_from, id_employee, rule_salary_current_month):

      type_struct_id = type_struct_id_employee
      
      struct_id = self.env['hr.payroll.structure'].search([('type_id','=',type_struct_id.id)],limit=1)

      payslips = self.env['hr.payslip'].sudo().search([('date_from','<',date_from),('struct_id','=',struct_id.id),
            ('employee_id', '=', id_employee)], limit=1, order="date_from")

      if rule_salary_current_month != self.value_rule(payslips.line_ids,'SB'):
        return True
      else:
        return False 
    #pension

    def pension_administrator_code(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            string = code
            break
        break
      return string

    def nit_pension_administrator(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            string = payslip.employee_id.pension_fund.nit.name
            break
        break
      return string

    def pension_administrator_verification_digit(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            string = payslip.employee_id.pension_fund.nit.code
            break
        break
      return string

    def total_value_of_mandatory_contributions_reported(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'PEN')+self.value_rule(payslip.line_ids,'PENP'),2))
      return total

    def total_value_of_voluntary_contributions_made_by_affiliates(self, code, payslip_run_id):
      total = 0

      return total

    def total_value_of_voluntary_contributions_made_by_the_contributor(self, code, payslip_run_id):
      total = 0

      return total

    def total_value_contributions_to_pension_solidarity_fund_solidarity_subaccount(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'FSP'),2))
      return total

    def total_value_contributions_to_pension_solidarity_fund_subsistence_subaccount(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'FST'),2))
      return total
    
    def total_affiliates_per_manager(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.pension_fund.code == code:
            total += 1
      return total

    def code_eps_or_eoc(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.eps_id.code == code:
            string = code
            break
        break
      return string

    def nit_of_the_eps_or_eoc(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.eps_id.code == code:
            string = payslip.employee_id.eps_id.nit.name
            break
        break
      return string

    def check_digit_eps_or_eoc(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.eps_id.code == code:
            string = payslip.employee_id.eps_id.nit.code
            break
        break
      return string

    def total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.eps_id.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'SAL'),2))
      return total

    def total_additional_upc_value_contributed_to_that_eps_or_eoc(self, code, payslip_run_id):
      total = 0
      return total

    def total_affiliates_by_eps_or_eoc(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.eps_id.code == code:
            total += 1
      return total

    def code_arl(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.arl_id.code == code:
            string = code
            break
        break
      return string

    def nit_de_la_arl(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.arl_id.code == code:
            string = payslip.employee_id.arl_id.nit.name
            break
        break
      return string

    def arl_check_digit(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.arl_id.code == code:
            string = payslip.employee_id.arl_id.nit.code
            break
        break
      return string

    def total_value_of_contributions_reported_to_that_manager(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.arl_id.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'ARLP'),2))
      return total

    def total_affiliates_per_manager(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.arl_id.code == code:
            total += 1
      return total
      
    def ccf_code(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.ccf_id.code == code:
            string = code
            break
        break
      return string

    def compulsory_identification_number_nit_of_the_ccf(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.ccf_id.code == code:
            string = payslip.employee_id.ccf_id.nit.name
            break
        break
      return string

    def ccf_check_digit(self, code, payslip_run_id):
      string = ''
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.ccf_id.code == code:
            string = payslip.employee_id.ccf_id.nit.code
            break
        break
      return string 

    def value_contribution_to_that_ccf(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.ccf_id.code == code:
            total += int(round(self.value_rule(payslip.line_ids,'CCFP'),2))
      return total

    def total_affiliates_per_ccf(self, code, payslip_run_id):
      total = 0
      for payslips in payslip_run_id:
        for payslip in payslips.slip_ids:
          if payslip.employee_id.ccf_id.code == code:
            total += 1
      return total


    def action_save_file(self):
        sfs_obj = self.env['plame.file.save']

        #str_encode = '\n'.join(self.get_output_lines()).encode('utf-8')
        #encoded_output_file = base64.encodestring(str_encode)
        str_encode_14= '\n'.join(self.estruct14()).encode('utf-8')
        encoded_output_file_14 = base64.encodebytes(str_encode_14)
        name_14 = 'Beneficios_Sociales'+str(self.year)+str(self.month)+str(self.ruc)+'.txt'
        str_encode_18= '\n'.join(self.estruct18()).encode('utf-8')
        encoded_output_file_18 = base64.encodebytes(str_encode_18)
        output_name_18 = '0601'+str(self.year)+str(self.month)+str(self.ruc)+'.rem'
        vals = {
            'output_name_14': name_14,
            'output_file_14': encoded_output_file_14,
            'output_name_18': output_name_18,
            'output_file_18': encoded_output_file_18,
        }
        sfs_id = sfs_obj.create(vals).id

        return {
            'name': ("GUARDAR ARCHIVO"),
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'plame.file.save',
            'res_id': sfs_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': ""
       }

    
    def estruct14(self):
        list_employees = []
        for i in self.payslip_run_id.slip_ids:
            for i2 in i.employee_id:
                list_employees.append(i2.name)

        total_employees = len(list(dict.fromkeys(list_employees)))

        sequence = 1

        current_date = fields.Datetime.context_timestamp(self,fields.Datetime.now())
        
        res = []
        lines_control_register_header = {}
        lines_detail_register_pension_employee = {}
        lines_detail_register_pension= {}
        lines_detail_register_eps = {}
        lines_detail_register_arl = {}
        lines_detail_register_ccf = {}


        
        total = 0

        for payslips in self.payslip_run_id:
            for payslip in payslips.slip_ids:
                for line in payslip.line_ids:
                    if line.category_id.code=='BSS':
                        total += line.total
        type_of_register = self.white_spaces('01',2,'left','0')
        modality_payroll = self.white_spaces('1',1,'left','0')
        number_sequence = self.white_spaces(sequence,4,'left','0')
        business_name_contributor = self.white_spaces(self.company_id.partner_id.name,200,'right',' ')
        type_document = self.white_spaces(self.company_id.partner_id.l10n_latam_identification_type_id.code,2,'right',' ') #consultar si es dinámico el campo
        taxpayer_identification_number = self.white_spaces(self.company_id.partner_id.vat[2:11],16,'right',' ')
        contributing_verification_digit = self.white_spaces(self.company_id.partner_id.check_digit,1,'left','0')
        type_of_spreadsheet = self.white_spaces('E',1,'right',' ')
        number_of_the_worksheet_associated = self.white_spaces('',10,'left','0')
        payment_date_associated_return = self.white_spaces('',10,'right',' ')
        form_of_presentation = self.white_spaces('U',1,'right',' ')
        taxpayer_branch_code = self.white_spaces('',10,'right',' ')
        branch_name = self.white_spaces('',40,'right',' ')
        contributing_arl_code = self.white_spaces(self.company_id.partner_id.arl_id.code,6,'right',' ')
        payment_period_for_non_health_systems = self.white_spaces(self.current_date.strftime("%Y-%m"),7,'right',' ')
        payment_period_health_system = self.white_spaces(self.current_date.strftime("%Y"),4,'left','0')+'-'+self.white_spaces(int(self.current_date.strftime("%m"))+1,2,'left','0')
        registration_number = self.white_spaces('',10,'left','0')
        payment_date = self.white_spaces('',10,'right',' ')
        total_number_of_employees = self.white_spaces(total_employees,5,'left','0')
        total_value_of_payroll = self.white_spaces(int(round(total,0)),12,'left','0')# CONSULTAR SI ES CATEGORÍA BSS
        type_of_contributor = self.white_spaces('1',2,'left','0')
        information_operator_code = self.white_spaces('86',2,'left','0')

    
        lines_control_register_header[1] = [
              self.convert_str(type_of_register),
              self.convert_str(modality_payroll),
              self.convert_str(number_sequence),
              self.convert_str(business_name_contributor),
              self.convert_str(type_document),
              self.convert_str(taxpayer_identification_number),
              self.convert_str(contributing_verification_digit),
              self.convert_str(type_of_spreadsheet),
              self.convert_str(number_of_the_worksheet_associated),
              self.convert_str(payment_date_associated_return),
              self.convert_str(form_of_presentation),
              self.convert_str(taxpayer_branch_code),
              self.convert_str(branch_name),
              self.convert_str(contributing_arl_code),
              self.convert_str(payment_period_for_non_health_systems),
              self.convert_str(payment_period_health_system),
              self.convert_str(registration_number),
              self.convert_str(payment_date),
              self.convert_str(total_number_of_employees),
              self.convert_str(total_value_of_payroll),
              self.convert_str(type_of_contributor),
              self.convert_str(information_operator_code),
              ]
        #VALIDACIÓN
        print("linea inicial")
        pos_i = 1
        pos_f = 1
        for i in lines_control_register_header[1]:
            pos_f = pos_i + len(i) -1
            print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
            pos_i = pos_f+1


        for x in lines_control_register_header:
          elements = [
              lines_control_register_header[x][0],
              lines_control_register_header[x][1],
              lines_control_register_header[x][2],
              lines_control_register_header[x][3],
              lines_control_register_header[x][4],
              lines_control_register_header[x][5],
              lines_control_register_header[x][6],
              lines_control_register_header[x][7],
              lines_control_register_header[x][8],
              lines_control_register_header[x][9],
              lines_control_register_header[x][10],
              lines_control_register_header[x][11],
              lines_control_register_header[x][12],
              lines_control_register_header[x][13],
              lines_control_register_header[x][14],
              lines_control_register_header[x][15],
              lines_control_register_header[x][16],
              lines_control_register_header[x][17],
              lines_control_register_header[x][18],
              lines_control_register_header[x][19],
              lines_control_register_header[x][20],
              lines_control_register_header[x][21],
          ]
          res.append(''.join(elements))
        
        list_pension = []
        list_eps = []
        list_arl = []
        list_ccf = []
        for payslips in self.payslip_run_id:
          for payslip in payslips.slip_ids:

              
              list_pension.append(payslip.employee_id.pension_fund.code)
              list_eps.append(payslip.employee_id.eps_id.code)
              list_arl.append(payslip.employee_id.arl_id.code)
              list_ccf.append(payslip.employee_id.ccf_id.code)
              
              type_of_register = self.white_spaces('02',2,'left','0')
              number_sequence = self.white_spaces('1',5,'left','0')
              type_of_contribution_document = self.white_spaces(payslip.employee_id.type_document_id.code,2,'right',' ')
              listing_identification_number = self.white_spaces(payslip.employee_id.identification_id,16,'right',' ')
              contributor_type = self.white_spaces(payslip.contract_id.type_contributor_id.code,2,'left','0')
              contributing_subtype = self.white_spaces(payslip.contract_id.subtype_contributor_id.code,2,'left','0')
              foreigner_not_obliged_to_contribute_to_pensions = self.white_spaces(self.validate_boolean(payslip.contract_id.foreigner_not_obliged_to_contribute_to_pensions),1,'right',' ')
              colombian_abroad = self.white_spaces(self.validate_boolean(payslip.contract_id.colombian_abroad),1,'right',' ')
              department_code_of_work_location = self.white_spaces(payslip.employee_id.address_home_id.department_id.code,2,'right',' ')
              municipality_code_of_work_location = self.white_spaces(str(payslip.employee_id.address_home_id.city_id.code)[2:5],3,'right',' ')
              surname = self.white_spaces(payslip.employee_id.last_name,20,'right',' ')
              second_surname = self.white_spaces(payslip.employee_id.mother_last_name,30,'right',' ')
              first_name = self.white_spaces(self.first_substring(payslip.employee_id.name),20,'right',' ')
              second_name = self.white_spaces(self.second_substring(payslip.employee_id.name),30,'right',' ')
              ing = self.white_spaces(self.entry_employee(payslip.contract_id.date_start,payslip.date_from),1,'right',' ')
              ret = self.white_spaces(self.exit_employee(payslip.contract_id.date_end,payslip.date_to),1,'right',' ')
              tde = self.white_spaces('',1,'right',' ')
              tae = self.white_spaces('',1,'right',' ')
              tdp = self.white_spaces('',1,'right',' ')
              tap = self.white_spaces('',1,'right',' ')
              
              vsp = self.white_spaces('',1,'right',' ')
              fixes = self.white_spaces('',1,'right',' ')
              vst = self.white_spaces('',1,'right',' ')
              sln = self.white_spaces('',1,'right',' ')
              ige = self.white_spaces('',1,'right',' ')
              lma = self.white_spaces('',1,'right',' ')
              vac_lr = self.white_spaces('',1,'right',' ')
              avp = self.white_spaces('',1,'right',' ')
              vct = self.white_spaces('',1,'right',' ')
              irl = self.white_spaces('',2,'left','0')
              affiliate_pension_fund_manager_code = self.white_spaces(payslip.employee_id.pension_fund.code,6,'right',' ')
              transfer_pension_fund_manager_code = self.white_spaces('',6,'right',' ')
              affiliate_eps_or_eoc_code = self.white_spaces(payslip.employee_id.eps_id.code,6,'right',' ')
              transfer_eps_or_eoc_code = self.white_spaces('',6,'right',' ')
              affiliate_ccf_code = self.white_spaces(payslip.employee_id.ccf_id.code,6,'right',' ')
              number_of_days_contributed_to_pension = self.white_spaces(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','DIAT')]).number_of_days),2,'left','0')
              number_of_days_paid_to_health = self.white_spaces(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','DIAT')]).number_of_days),2,'left','0')
              number_of_days_quoted_to_occupational_risks = self.white_spaces(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','DIAT')]).number_of_days),2,'left','0')
              number_of_days_contributed_to_the_family_compensation_fund = self.white_spaces('0',2,'left','0')
              basic_salary = self.white_spaces(int(round(payslip.contract_id.wage,2)),9,'left','0')
              integral_salary = self.white_spaces(self.is_integral_salary(payslip.struct_id.id),1,'right',' ')
              ibc_pension = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'IBCS'),2)),9,'left','0')
              ibc_health = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'IBCS'),2)),9,'left','0')
              ibc_occupational_risks = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'IBCA'),2)),9,'left','0')
              ibc_ccf = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'IBCP'),2)),9,'left','0')
              pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
              mandatory_pension_contribution = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'PEN')+self.value_rule(payslip.line_ids,'PENP'),2)),9,'left','0')
              voluntary_contribution_of_the_member_to_the_mandatory_pension_fund = self.white_spaces('',9,'left','0')
              voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund = self.white_spaces('',9,'left','0')
              total_contribution_of_the_general_pension_system = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'PEN')+self.value_rule(payslip.line_ids,'PENP'),2)),9,'left','0')
              contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'FSP'),2)),9,'left','0')
              contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'FST'),2)),9,'left','0')
              value_not_retained_by_voluntary_contributions = self.white_spaces('',9,'left','0')
              health_contribution_rate = self.white_spaces(self.health_contribution_rate(payslip.contract_id.wage,payslip.date_from),7,'right','0')
              mandatory_contribution_to_health = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'SAL'),2)),9,'left','0')
              additional_upc_value = self.white_spaces('',9,'left','0')
              authorization_number_of_disability_due_to_general_illness = self.white_spaces('',15,'right',' ')
              value_of_disability_due_to_general_illness = self.white_spaces('',9,'left','0')
              authorization_number_of_the_maternity_or_paternity_leave = self.white_spaces('',15,'right',' ')
              value_of_maternity_leave = self.white_spaces('',9,'left','0')
              rate_of_contributions_to_occupational_risks = self.white_spaces(float(payslip.contract_id.type_risk_arl_id.name)/100,9,'right','0')
              workplace = self.white_spaces(str(payslip.contract_id.company_id.partner_id.vat)[2:11],9,'left','0')
              mandatory_contribution_to_the_general_system_of_occupational_hazards = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'ARLP'),2)),9,'left','0')
              
              contribution_rate_ccf = self.white_spaces('0.04',7,'right','0')
              contribution_value_ccf = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'CCFP'),2)),9,'left','0')
              sena_contribution_fee = self.white_spaces(self.condition_senp(self.value_category_rule(payslip.line_ids,'DSS'),payslip.date_from),7,'right','0')
              sena_contribution_value = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'SENP'),2)),9,'left','0')
              icbf_contribution_rate = self.white_spaces(self.condition_icbp(self.value_category_rule(payslip.line_ids,'DSS'),payslip.date_from),7,'right','0')
              icbf_contribution_value = self.white_spaces(int(round(self.value_rule(payslip.line_ids,'ICBP'),2)),9,'left','0')
              esap_contribution_rate = self.white_spaces('0.0',7,'right','0')
              esap_contribution_value = self.white_spaces('0',9,'left','0')
              men_contribution_rate = self.white_spaces('0.0',7,'right','0')
              men_contribution_value = self.white_spaces('0',9,'left','0')
              document_type_of_the_main_contributor = self.white_spaces('',2,'right',' ')
              identification_number_of_the_main_contributor = self.white_spaces('',16,'right',' ')
              contributor_exempted_from_payment_of_health_contribution_sena_and_icbf = self.white_spaces(self.contributing_condition_exonerated(self.value_rule(payslip.line_ids,'IBCS'),payslip.date_from),1,'right',' ')
              code_of_the_occupational_risk_manager_to_which_the_member_belongs = self.white_spaces(payslip.employee_id.arl_id.code,6,'right',' ')
              risk_class_in_which_the_affiliate_is = self.white_spaces(payslip.contract_id.type_risk_arl_id.code,1,'right',' ')
              pension_special_rate_indicator = self.white_spaces(self.pension_special_rate_indicator(payslip.contract_id.type_employee.name),1,'right',' ')
              date_of_admission = self.white_spaces(self.date_entry(self.entry_employee(payslip.contract_id.date_start,payslip.date_from),payslip.contract_id.date_start),10,'right',' ')
              retirement_date = self.white_spaces(self.date_exit(self.exit_employee(payslip.contract_id.date_end,payslip.date_to),payslip.contract_id.date_end),10,'right',' ')
              vsp_start_date = self.white_spaces('',10,'right',' ')
              sln_start_date = self.white_spaces('',10,'right',' ')
              end_date_sln = self.white_spaces('',10,'right',' ')
              start_date_ige = self.white_spaces('',10,'right',' ')
              end_date_ige = self.white_spaces('',10,'right',' ')
              start_date_lma = self.white_spaces('',10,'right',' ')
              end_date_lma = self.white_spaces('',10,'right',' ')
              start_date_vac_lr = self.white_spaces('',10,'right',' ')
              end_date_vac_lr = self.white_spaces('',10,'right',' ')
              start_date_vct = self.white_spaces('',10,'right',' ')
              end_date_vct = self.white_spaces('',10,'right',' ')
              start_date_irl = self.white_spaces('',10,'right',' ')
              finirl_date = self.white_spaces('',10,'right',' ')
              ibc_other_parafiscals_other_than_ccf = self.white_spaces(self.ibc_other_parafiscals_other_than_ccf(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf,self.value_rule(payslip.line_ids,'IBCP')),9,'left','0')
              number_of_hours_worked = self.white_spaces(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','DIAT')]).number_of_hours),3,'left','0')


              code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
              

              lines_detail_register_pension_employee[code] = [
                    self.convert_str(type_of_register),
                    self.convert_str(number_sequence),
                    self.convert_str(type_of_contribution_document),
                    self.convert_str(listing_identification_number),
                    self.convert_str(contributor_type),
                    self.convert_str(contributing_subtype),
                    self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                    self.convert_str(colombian_abroad),
                    self.convert_str(department_code_of_work_location),
                    self.convert_str(municipality_code_of_work_location),
                    self.convert_str(surname),
                    self.convert_str(second_surname),
                    self.convert_str(first_name),
                    self.convert_str(second_name),
                    self.convert_str(ing),
                    self.convert_str(ret),
                    self.convert_str(tde),
                    self.convert_str(tae),
                    self.convert_str(tdp),
                    self.convert_str(tap),
                    self.convert_str(vsp),
                    self.convert_str(fixes),
                    self.convert_str(vst),
                    self.convert_str(sln),
                    self.convert_str(ige),
                    self.convert_str(lma),
                    self.convert_str(vac_lr),
                    self.convert_str(avp),
                    self.convert_str(vct),
                    self.convert_str(irl),
                    self.convert_str(affiliate_pension_fund_manager_code),
                    self.convert_str(transfer_pension_fund_manager_code),
                    self.convert_str(affiliate_eps_or_eoc_code),
                    self.convert_str(transfer_eps_or_eoc_code),
                    self.convert_str(affiliate_ccf_code),
                    self.convert_str(number_of_days_contributed_to_pension),
                    self.convert_str(number_of_days_paid_to_health),
                    self.convert_str(number_of_days_quoted_to_occupational_risks),
                    self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                    self.convert_str(basic_salary),
                    self.convert_str(integral_salary),
                    self.convert_str(ibc_pension),
                    self.convert_str(ibc_health),
                    self.convert_str(ibc_occupational_risks),
                    self.convert_str(ibc_ccf),
                    self.convert_str(pension_contribution_rate),
                    self.convert_str(mandatory_pension_contribution),
                    self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                    self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                    self.convert_str(total_contribution_of_the_general_pension_system),
                    self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                    self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                    self.convert_str(value_not_retained_by_voluntary_contributions),
                    self.convert_str(health_contribution_rate),
                    self.convert_str(mandatory_contribution_to_health),
                    self.convert_str(additional_upc_value),
                    self.convert_str(authorization_number_of_disability_due_to_general_illness),
                    self.convert_str(value_of_disability_due_to_general_illness),
                    self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                    self.convert_str(value_of_maternity_leave),
                    self.convert_str(rate_of_contributions_to_occupational_risks),
                    self.convert_str(workplace),
                    self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                    self.convert_str(contribution_rate_ccf),
                    self.convert_str(contribution_value_ccf),
                    self.convert_str(sena_contribution_fee),
                    self.convert_str(sena_contribution_value),
                    self.convert_str(icbf_contribution_rate),
                    self.convert_str(icbf_contribution_value),
                    self.convert_str(esap_contribution_rate),
                    self.convert_str(esap_contribution_value),
                    self.convert_str(men_contribution_rate),
                    self.convert_str(men_contribution_value),
                    self.convert_str(document_type_of_the_main_contributor),
                    self.convert_str(identification_number_of_the_main_contributor),
                    self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                    self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                    self.convert_str(risk_class_in_which_the_affiliate_is),
                    self.convert_str(pension_special_rate_indicator),
                    self.convert_str(date_of_admission),
                    self.convert_str(retirement_date),
                    self.convert_str(vsp_start_date),
                    self.convert_str(sln_start_date),
                    self.convert_str(end_date_sln),
                    self.convert_str(start_date_ige),
                    self.convert_str(end_date_ige),
                    self.convert_str(start_date_lma),
                    self.convert_str(end_date_lma),
                    self.convert_str(start_date_vac_lr),
                    self.convert_str(end_date_vac_lr),
                    self.convert_str(start_date_vct),
                    self.convert_str(end_date_vct),
                    self.convert_str(start_date_irl),
                    self.convert_str(finirl_date),
                    self.convert_str(ibc_other_parafiscals_other_than_ccf),
                    self.convert_str(number_of_hours_worked),
                    ]
              # NOVEDAD DE VSP -FALTA PONER LA FECHA DE CAMBIO DE SUELDO
              orden = 1
              if self.permanent_variation_of_salary(payslip.contract_id.structure_type_id, payslip.date_from, payslip.employee_id.id, self.value_rule(payslip.line_ids,'SB')):
                
                vsp = self.white_spaces('X',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')
       
                
                lines_detail_register_pension_employee[int(code)+orden] = [
                      self.convert_str(type_of_register),
                      self.convert_str(number_sequence),
                      self.convert_str(type_of_contribution_document),
                      self.convert_str(listing_identification_number),
                      self.convert_str(contributor_type),
                      self.convert_str(contributing_subtype),
                      self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                      self.convert_str(colombian_abroad),
                      self.convert_str(department_code_of_work_location),
                      self.convert_str(municipality_code_of_work_location),
                      self.convert_str(surname),
                      self.convert_str(second_surname),
                      self.convert_str(first_name),
                      self.convert_str(second_name),
                      self.convert_str(ing),
                      self.convert_str(ret),
                      self.convert_str(tde),
                      self.convert_str(tae),
                      self.convert_str(tdp),
                      self.convert_str(tap),
                      self.convert_str(vsp),
                      self.convert_str(fixes),
                      self.convert_str(vst),
                      self.convert_str(sln),
                      self.convert_str(ige),
                      self.convert_str(lma),
                      self.convert_str(vac_lr),
                      self.convert_str(avp),
                      self.convert_str(vct),
                      self.convert_str(irl),
                      self.convert_str(affiliate_pension_fund_manager_code),
                      self.convert_str(transfer_pension_fund_manager_code),
                      self.convert_str(affiliate_eps_or_eoc_code),
                      self.convert_str(transfer_eps_or_eoc_code),
                      self.convert_str(affiliate_ccf_code),
                      self.convert_str(number_of_days_contributed_to_pension),
                      self.convert_str(number_of_days_paid_to_health),
                      self.convert_str(number_of_days_quoted_to_occupational_risks),
                      self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                      self.convert_str(basic_salary),
                      self.convert_str(integral_salary),
                      self.convert_str(ibc_pension),
                      self.convert_str(ibc_health),
                      self.convert_str(ibc_occupational_risks),
                      self.convert_str(ibc_ccf),
                      self.convert_str(pension_contribution_rate),
                      self.convert_str(mandatory_pension_contribution),
                      self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                      self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                      self.convert_str(total_contribution_of_the_general_pension_system),
                      self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                      self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                      self.convert_str(value_not_retained_by_voluntary_contributions),
                      self.convert_str(health_contribution_rate),
                      self.convert_str(mandatory_contribution_to_health),
                      self.convert_str(additional_upc_value),
                      self.convert_str(authorization_number_of_disability_due_to_general_illness),
                      self.convert_str(value_of_disability_due_to_general_illness),
                      self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                      self.convert_str(value_of_maternity_leave),
                      self.convert_str(rate_of_contributions_to_occupational_risks),
                      self.convert_str(workplace),
                      self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                      self.convert_str(contribution_rate_ccf),
                      self.convert_str(contribution_value_ccf),
                      self.convert_str(sena_contribution_fee),
                      self.convert_str(sena_contribution_value),
                      self.convert_str(icbf_contribution_rate),
                      self.convert_str(icbf_contribution_value),
                      self.convert_str(esap_contribution_rate),
                      self.convert_str(esap_contribution_value),
                      self.convert_str(men_contribution_rate),
                      self.convert_str(men_contribution_value),
                      self.convert_str(document_type_of_the_main_contributor),
                      self.convert_str(identification_number_of_the_main_contributor),
                      self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                      self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                      self.convert_str(risk_class_in_which_the_affiliate_is),
                      self.convert_str(pension_special_rate_indicator),
                      self.convert_str(date_of_admission),
                      self.convert_str(retirement_date),
                      self.convert_str(vsp_start_date),
                      self.convert_str(sln_start_date),
                      self.convert_str(end_date_sln),
                      self.convert_str(start_date_ige),
                      self.convert_str(end_date_ige),
                      self.convert_str(start_date_lma),
                      self.convert_str(end_date_lma),
                      self.convert_str(start_date_vac_lr),
                      self.convert_str(end_date_vac_lr),
                      self.convert_str(start_date_vct),
                      self.convert_str(end_date_vct),
                      self.convert_str(start_date_irl),
                      self.convert_str(finirl_date),
                      self.convert_str(ibc_other_parafiscals_other_than_ccf),
                      self.convert_str(number_of_hours_worked),
                      ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE VSP")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1



              # NOVEDAD DE SLN 
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','SLN')]).number_of_days))>0 or self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','ANR')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('X',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.12',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                #sln_start_date = self.white_spaces('',10,'right',' ')
                #end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')
                

                list_sln = ['sln', 'lnr']
                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','in',list_sln),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    sln_start_date = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_sln = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')

            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDADES DE SLN")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

              # NOVEDAD DE IGE 
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','IGE')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('X',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                #start_date_ige = self.white_spaces('',10,'right',' ')
                #end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','=','ige'),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_ige = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_ige = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE IGE")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

              # NOVEDAD DE LMA 
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','LMA')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('X',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                #start_date_lma = self.white_spaces('',10,'right',' ')
                #end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','=','lma'),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_lma = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_lma = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE LMA")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

              # NOVEDAD DE LPA 
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','LPA')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('X',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                #start_date_lma = self.white_spaces('',10,'right',' ')
                #end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','=','lpa'),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_lma = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_lma = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE LPA")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

              # NOVEDAD DE VAC 
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','VCO')]).number_of_days))>0 or self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','VDI')]).number_of_days))>0 or self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','VRE')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('X',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                #start_date_vac_lr = self.white_spaces('',10,'right',' ')
                #end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                list_vac = ['vco','vdi','vre']
                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','in',list_vac),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_vac_lr = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_vac_lr = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE VAC")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

              # NOVEDAD DE LR
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','LR')]).number_of_days))>0 or self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','LT')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('X',1,'right',' ')
                irl = self.white_spaces('',2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                #start_date_vac_lr = self.white_spaces('',10,'right',' ')
                #end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                start_date_irl = self.white_spaces('',10,'right',' ')
                finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','in',['lr','lt']),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_vac_lr = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    end_date_vac_lr = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE LR")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1
              
              # NOVEDAD DE IRL
              
              if self.validate_novelty_sln(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','IRL')]).number_of_days))>0:
                
                vsp = self.white_spaces('',1,'right',' ')
                sln = self.white_spaces('',1,'right',' ')
                ige = self.white_spaces('',1,'right',' ')
                lma = self.white_spaces('',1,'right',' ')
                vac_lr = self.white_spaces('',1,'right',' ')
                irl = self.white_spaces(int(self.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id),('code','=','IRL')]).number_of_days),2,'left','0')
                ibc_pension = self.white_spaces('',9,'left','0')
                ibc_health = self.white_spaces('',9,'left','0')
                ibc_occupational_risks = self.white_spaces('',9,'left','0')
                pension_contribution_rate = self.white_spaces('0.16',7,'right','0') #CAMBIA PARA LA NOV LIC NO REMUNERADA
                mandatory_pension_contribution = self.white_spaces('',9,'left','0')
                total_contribution_of_the_general_pension_system = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',9,'left','0')
                contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',9,'left','0')
                mandatory_contribution_to_health = self.white_spaces('',9,'left','0')
                rate_of_contributions_to_occupational_risks = self.white_spaces('',9,'right','0')
                date_of_admission = self.white_spaces('',10,'right',' ')
                retirement_date = self.white_spaces('',10,'right',' ')
                vsp_start_date = self.white_spaces('',10,'right',' ') # FALTA CREAR EL METODO PARA CAPTURAR LA FECHA CUANDO SE ACTUALIZA EL SALARIO
                sln_start_date = self.white_spaces('',10,'right',' ')
                end_date_sln = self.white_spaces('',10,'right',' ')
                start_date_ige = self.white_spaces('',10,'right',' ')
                end_date_ige = self.white_spaces('',10,'right',' ')
                start_date_lma = self.white_spaces('',10,'right',' ')
                end_date_lma = self.white_spaces('',10,'right',' ')
                start_date_vac_lr = self.white_spaces('',10,'right',' ')
                end_date_vac_lr = self.white_spaces('',10,'right',' ')
                start_date_vct = self.white_spaces('',10,'right',' ')
                end_date_vct = self.white_spaces('',10,'right',' ')
                #start_date_irl = self.white_spaces('',10,'right',' ')
                #finirl_date = self.white_spaces('',10,'right',' ')
                number_of_hours_worked = self.white_spaces('',3,'left','0')


                leaves = line.env['hr.leave'].search([('request_date_from','>=',payslip.date_from),
                    ('request_date_to','<=',payslip.date_to),('state','=','validate'),
                    ('holiday_status_id.novelty','=','irl'),('employee_id','=',payslip.employee_id.id)])

                if leaves:
                  for leave in leaves:
                    orden += 1
                    start_date_irl = self.white_spaces(leave.request_date_from.strftime("%Y-%m-%d"),10,'right',' ')
                    finirl_date = self.white_spaces(leave.request_date_to.strftime("%Y-%m-%d"),10,'right',' ')
                    
            
                    lines_detail_register_pension_employee[int(code)+orden] = [
                          self.convert_str(type_of_register),
                          self.convert_str(number_sequence),
                          self.convert_str(type_of_contribution_document),
                          self.convert_str(listing_identification_number),
                          self.convert_str(contributor_type),
                          self.convert_str(contributing_subtype),
                          self.convert_str(foreigner_not_obliged_to_contribute_to_pensions),
                          self.convert_str(colombian_abroad),
                          self.convert_str(department_code_of_work_location),
                          self.convert_str(municipality_code_of_work_location),
                          self.convert_str(surname),
                          self.convert_str(second_surname),
                          self.convert_str(first_name),
                          self.convert_str(second_name),
                          self.convert_str(ing),
                          self.convert_str(ret),
                          self.convert_str(tde),
                          self.convert_str(tae),
                          self.convert_str(tdp),
                          self.convert_str(tap),
                          self.convert_str(vsp),
                          self.convert_str(fixes),
                          self.convert_str(vst),
                          self.convert_str(sln),
                          self.convert_str(ige),
                          self.convert_str(lma),
                          self.convert_str(vac_lr),
                          self.convert_str(avp),
                          self.convert_str(vct),
                          self.convert_str(irl),
                          self.convert_str(affiliate_pension_fund_manager_code),
                          self.convert_str(transfer_pension_fund_manager_code),
                          self.convert_str(affiliate_eps_or_eoc_code),
                          self.convert_str(transfer_eps_or_eoc_code),
                          self.convert_str(affiliate_ccf_code),
                          self.convert_str(number_of_days_contributed_to_pension),
                          self.convert_str(number_of_days_paid_to_health),
                          self.convert_str(number_of_days_quoted_to_occupational_risks),
                          self.convert_str(number_of_days_contributed_to_the_family_compensation_fund),
                          self.convert_str(basic_salary),
                          self.convert_str(integral_salary),
                          self.convert_str(ibc_pension),
                          self.convert_str(ibc_health),
                          self.convert_str(ibc_occupational_risks),
                          self.convert_str(ibc_ccf),
                          self.convert_str(pension_contribution_rate),
                          self.convert_str(mandatory_pension_contribution),
                          self.convert_str(voluntary_contribution_of_the_member_to_the_mandatory_pension_fund),
                          self.convert_str(voluntary_contribution_of_the_contributor_to_the_mandatory_pension_fund),
                          self.convert_str(total_contribution_of_the_general_pension_system),
                          self.convert_str(contributions_to_pension_solidarity_fund_solidarity_subaccount),
                          self.convert_str(contributions_to_pension_solidarity_fund_subsistence_subaccount),
                          self.convert_str(value_not_retained_by_voluntary_contributions),
                          self.convert_str(health_contribution_rate),
                          self.convert_str(mandatory_contribution_to_health),
                          self.convert_str(additional_upc_value),
                          self.convert_str(authorization_number_of_disability_due_to_general_illness),
                          self.convert_str(value_of_disability_due_to_general_illness),
                          self.convert_str(authorization_number_of_the_maternity_or_paternity_leave),
                          self.convert_str(value_of_maternity_leave),
                          self.convert_str(rate_of_contributions_to_occupational_risks),
                          self.convert_str(workplace),
                          self.convert_str(mandatory_contribution_to_the_general_system_of_occupational_hazards),
                          self.convert_str(contribution_rate_ccf),
                          self.convert_str(contribution_value_ccf),
                          self.convert_str(sena_contribution_fee),
                          self.convert_str(sena_contribution_value),
                          self.convert_str(icbf_contribution_rate),
                          self.convert_str(icbf_contribution_value),
                          self.convert_str(esap_contribution_rate),
                          self.convert_str(esap_contribution_value),
                          self.convert_str(men_contribution_rate),
                          self.convert_str(men_contribution_value),
                          self.convert_str(document_type_of_the_main_contributor),
                          self.convert_str(identification_number_of_the_main_contributor),
                          self.convert_str(contributor_exempted_from_payment_of_health_contribution_sena_and_icbf),
                          self.convert_str(code_of_the_occupational_risk_manager_to_which_the_member_belongs),
                          self.convert_str(risk_class_in_which_the_affiliate_is),
                          self.convert_str(pension_special_rate_indicator),
                          self.convert_str(date_of_admission),
                          self.convert_str(retirement_date),
                          self.convert_str(vsp_start_date),
                          self.convert_str(sln_start_date),
                          self.convert_str(end_date_sln),
                          self.convert_str(start_date_ige),
                          self.convert_str(end_date_ige),
                          self.convert_str(start_date_lma),
                          self.convert_str(end_date_lma),
                          self.convert_str(start_date_vac_lr),
                          self.convert_str(end_date_vac_lr),
                          self.convert_str(start_date_vct),
                          self.convert_str(end_date_vct),
                          self.convert_str(start_date_irl),
                          self.convert_str(finirl_date),
                          self.convert_str(ibc_other_parafiscals_other_than_ccf),
                          self.convert_str(number_of_hours_worked),
                          ]
              #VALIDACIÓN
              print("lineas nominas NOVEDAD DE IRL")
              pos_i = 1
              pos_f = 1
              for i in lines_detail_register_pension_employee[int(code)+orden]:
                  pos_f = pos_i + len(i) -1
                  print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
                  pos_i = pos_f+1

        for x in lines_detail_register_pension_employee:
          elements = [
              lines_detail_register_pension_employee[x][0],
              lines_detail_register_pension_employee[x][1],
              lines_detail_register_pension_employee[x][2],
              lines_detail_register_pension_employee[x][3],
              lines_detail_register_pension_employee[x][4],
              lines_detail_register_pension_employee[x][5],
              lines_detail_register_pension_employee[x][6],
              lines_detail_register_pension_employee[x][7],
              lines_detail_register_pension_employee[x][8],
              lines_detail_register_pension_employee[x][9],
              lines_detail_register_pension_employee[x][10],
              lines_detail_register_pension_employee[x][11],
              lines_detail_register_pension_employee[x][12],
              lines_detail_register_pension_employee[x][13],
              lines_detail_register_pension_employee[x][14],
              lines_detail_register_pension_employee[x][15],
              lines_detail_register_pension_employee[x][16],
              lines_detail_register_pension_employee[x][17],
              lines_detail_register_pension_employee[x][18],
              lines_detail_register_pension_employee[x][19],
              lines_detail_register_pension_employee[x][20],
              lines_detail_register_pension_employee[x][21],
              lines_detail_register_pension_employee[x][22],
              lines_detail_register_pension_employee[x][23],
              lines_detail_register_pension_employee[x][24],
              lines_detail_register_pension_employee[x][25],
              lines_detail_register_pension_employee[x][26],
              lines_detail_register_pension_employee[x][27],
              lines_detail_register_pension_employee[x][28],
              lines_detail_register_pension_employee[x][29],
              lines_detail_register_pension_employee[x][30],
              lines_detail_register_pension_employee[x][31],
              lines_detail_register_pension_employee[x][32],
              lines_detail_register_pension_employee[x][33],
              lines_detail_register_pension_employee[x][34],
              lines_detail_register_pension_employee[x][35],
              lines_detail_register_pension_employee[x][36],
              lines_detail_register_pension_employee[x][37],
              lines_detail_register_pension_employee[x][38],
              lines_detail_register_pension_employee[x][39],
              lines_detail_register_pension_employee[x][40],
              lines_detail_register_pension_employee[x][41],
              lines_detail_register_pension_employee[x][42],
              lines_detail_register_pension_employee[x][43],
              lines_detail_register_pension_employee[x][44],
              lines_detail_register_pension_employee[x][45],
              lines_detail_register_pension_employee[x][46],
              lines_detail_register_pension_employee[x][47],
              lines_detail_register_pension_employee[x][48],
              lines_detail_register_pension_employee[x][49],
              lines_detail_register_pension_employee[x][50],
              lines_detail_register_pension_employee[x][51],
              lines_detail_register_pension_employee[x][52],
              lines_detail_register_pension_employee[x][53],
              lines_detail_register_pension_employee[x][54],
              lines_detail_register_pension_employee[x][55],
              lines_detail_register_pension_employee[x][56],
              lines_detail_register_pension_employee[x][57],
              lines_detail_register_pension_employee[x][58],
              lines_detail_register_pension_employee[x][59],
              lines_detail_register_pension_employee[x][60],
              lines_detail_register_pension_employee[x][61],
              lines_detail_register_pension_employee[x][62],
              lines_detail_register_pension_employee[x][63],
              lines_detail_register_pension_employee[x][64],
              lines_detail_register_pension_employee[x][65],
              lines_detail_register_pension_employee[x][66],
              lines_detail_register_pension_employee[x][67],
              lines_detail_register_pension_employee[x][68],
              lines_detail_register_pension_employee[x][69],
              lines_detail_register_pension_employee[x][70],
              lines_detail_register_pension_employee[x][71],
              lines_detail_register_pension_employee[x][72],
              lines_detail_register_pension_employee[x][73],
              lines_detail_register_pension_employee[x][74],
              lines_detail_register_pension_employee[x][75],
              lines_detail_register_pension_employee[x][76],
              lines_detail_register_pension_employee[x][77],
              lines_detail_register_pension_employee[x][78],
              lines_detail_register_pension_employee[x][79],
              lines_detail_register_pension_employee[x][80],
              lines_detail_register_pension_employee[x][81],
              lines_detail_register_pension_employee[x][82],
              lines_detail_register_pension_employee[x][83],
              lines_detail_register_pension_employee[x][84],
              lines_detail_register_pension_employee[x][85],
              lines_detail_register_pension_employee[x][86],
              lines_detail_register_pension_employee[x][87],
              lines_detail_register_pension_employee[x][88],
              lines_detail_register_pension_employee[x][89],
              lines_detail_register_pension_employee[x][90],
              lines_detail_register_pension_employee[x][91],
              lines_detail_register_pension_employee[x][92],
              lines_detail_register_pension_employee[x][93],
              lines_detail_register_pension_employee[x][94],
              lines_detail_register_pension_employee[x][95],
          ]
          res.append(''.join(elements))
        
        #REGISTRO TIPO 3. TOTAL APORTES DEL PERÍODO PARA PENSIONES

        list_unique_pension = list(dict.fromkeys(list_pension))
        
        sequence = 0
        for pension in list_unique_pension:
          orden += 1
          sequence += 1
          type_of_register = self.white_spaces('03',2,'left','0')
          number_sequence = self.white_spaces(sequence,5,'left','0')
          pension_administrator_code = self.white_spaces(self.pension_administrator_code(pension,self.payslip_run_id),6,'right',' ')
          nit_pension_administrator = self.white_spaces(self.nit_pension_administrator(pension,self.payslip_run_id),16,'right',' ')
          pension_administrator_verification_digit = self.white_spaces(self.pension_administrator_verification_digit(pension,self.payslip_run_id),1,'left','0')
          total_value_of_mandatory_contributions_reported = self.white_spaces(self.total_value_of_mandatory_contributions_reported(pension,self.payslip_run_id),13,'left','0')
          total_value_of_voluntary_contributions_made_by_affiliates = self.white_spaces(self.total_value_of_voluntary_contributions_made_by_affiliates(pension,self.payslip_run_id),13,'left','0')
          total_value_of_voluntary_contributions_made_by_the_contributor = self.white_spaces(self.total_value_of_voluntary_contributions_made_by_the_contributor(pension,self.payslip_run_id),13,'left','0')
          total_value_contributions_to_pension_solidarity_fund_solidarity_subaccount = self.white_spaces(self.total_value_contributions_to_pension_solidarity_fund_solidarity_subaccount(pension,self.payslip_run_id),13,'left','0')
          total_value_contributions_to_pension_solidarity_fund_subsistence_subaccount = self.white_spaces(self.total_value_contributions_to_pension_solidarity_fund_subsistence_subaccount(pension,self.payslip_run_id),13,'left','0')
          number_of_days_past_due_settled = self.white_spaces('',4,'left','0')
          value_of_default_interest_on_the_total_value_of_the_quotations_for_the_period_settled = self.white_spaces('',11,'left','0')
          value_of_default_interest_on_the_total_value_of_contribution_to_the_pension_solidarity_fund_solidarity_subaccount = self.white_spaces('',11,'left','0')
          value_of_default_interest_on_the_total_value_contribution_pension_solidarity_fund_subsistence_subaccount = self.white_spaces('',11,'left','0')
          total_to_be_paid_to_the_administrator = self.white_spaces(self.total_value_of_mandatory_contributions_reported(pension,self.payslip_run_id)+self.total_value_of_voluntary_contributions_made_by_affiliates(pension,self.payslip_run_id)+self.total_value_of_voluntary_contributions_made_by_the_contributor(pension,self.payslip_run_id)+self.total_value_contributions_to_pension_solidarity_fund_solidarity_subaccount(pension,self.payslip_run_id)+self.total_value_contributions_to_pension_solidarity_fund_subsistence_subaccount(pension,self.payslip_run_id),13,'left','0')

          total_affiliates_per_manager = self.white_spaces(self.total_affiliates_per_manager(pension,self.payslip_run_id),8,'left','0')


          code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
          
          lines_detail_register_pension[int(code)+orden] = [
                self.convert_str(type_of_register),
                self.convert_str(number_sequence),
                self.convert_str(pension_administrator_code),
                self.convert_str(nit_pension_administrator),
                self.convert_str(pension_administrator_verification_digit),
                self.convert_str(total_value_of_mandatory_contributions_reported),
                self.convert_str(total_value_of_voluntary_contributions_made_by_affiliates),
                self.convert_str(total_value_of_voluntary_contributions_made_by_the_contributor),
                self.convert_str(total_value_contributions_to_pension_solidarity_fund_solidarity_subaccount),
                self.convert_str(total_value_contributions_to_pension_solidarity_fund_subsistence_subaccount),
                self.convert_str(number_of_days_past_due_settled),
                self.convert_str(value_of_default_interest_on_the_total_value_of_the_quotations_for_the_period_settled),
                self.convert_str(value_of_default_interest_on_the_total_value_of_contribution_to_the_pension_solidarity_fund_solidarity_subaccount),
                self.convert_str(value_of_default_interest_on_the_total_value_contribution_pension_solidarity_fund_subsistence_subaccount),
                self.convert_str(total_to_be_paid_to_the_administrator),
                self.convert_str(total_affiliates_per_manager),

                ]
          #VALIDACIÓN
          print("lineas nominas REGISTRO TIPO 3. TOTAL APORTES DEL PERÍODO PARA PENSIONES")
          pos_i = 1
          pos_f = 1
          for i in lines_detail_register_pension[int(code)+orden]:
              pos_f = pos_i + len(i) -1
              print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
              pos_i = pos_f+1


             

        for x in lines_detail_register_pension:
            elements = [
                lines_detail_register_pension[x][0],
                lines_detail_register_pension[x][1],
                lines_detail_register_pension[x][2],
                lines_detail_register_pension[x][3],
                lines_detail_register_pension[x][4],
                lines_detail_register_pension[x][5],
                lines_detail_register_pension[x][6],
                lines_detail_register_pension[x][7],
                lines_detail_register_pension[x][8],
                lines_detail_register_pension[x][9],
                lines_detail_register_pension[x][10],
                lines_detail_register_pension[x][11],
                lines_detail_register_pension[x][12],
                lines_detail_register_pension[x][13],
                lines_detail_register_pension[x][14],
                lines_detail_register_pension[x][15],
            ]
            res.append(''.join(elements))

        #REGISTRO TIPO 5. TOTAL APORTES DEL PERÍODO PARA SALUD

        list_unique_eps = list(dict.fromkeys(list_eps))
        sequence = 0
        for eps in list_unique_eps:
          orden += 1
          sequence += 1
          type_of_register = self.white_spaces('05',2,'left','0')
          number_sequence = self.white_spaces(sequence,5,'left','0')
          code_eps_or_eoc = self.white_spaces(self.code_eps_or_eoc(eps,self.payslip_run_id),6,'right',' ')
          nit_of_the_eps_or_eoc = self.white_spaces(self.nit_of_the_eps_or_eoc(eps,self.payslip_run_id),16,'right',' ')
          check_digit_eps_or_eoc = self.white_spaces(self.check_digit_eps_or_eoc(eps,self.payslip_run_id),1,'left','0')
          total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc = self.white_spaces(self.total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          total_additional_upc_value_contributed_to_that_eps_or_eoc = self.white_spaces(self.total_additional_upc_value_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          net_value_contributions_quote = self.white_spaces(self.total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          number_of_days_past_due_settled = self.white_spaces('',4,'left','0')
          value_interest_on_arrears_mandatory_contributions = self.white_spaces('',11,'left','0')
          value_of_additional_interest_on_arrears_upc = self.white_spaces('',11,'left','0')
          subtotal_contributions_contribution = self.white_spaces(self.total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          subtotal_additional_upc_contributions = self.white_spaces('',13,'left','0')
          total_to_pay_for_mandatory_quotation = self.white_spaces(self.total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          total_to_pay_for_additional_upc = self.white_spaces('',13,'left','0')
          total_to_be_paid_to_the_administrator = self.white_spaces(self.total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc(eps,self.payslip_run_id),13,'left','0')
          total_affiliates_by_eps_or_eoc = self.white_spaces(self.total_affiliates_by_eps_or_eoc(eps,self.payslip_run_id),8,'left','0')



          code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
          
          lines_detail_register_eps[int(code)+orden] = [
                self.convert_str(type_of_register),
                self.convert_str(number_sequence),
                self.convert_str(code_eps_or_eoc),
                self.convert_str(nit_of_the_eps_or_eoc),
                self.convert_str(check_digit_eps_or_eoc),
                self.convert_str(total_value_of_mandatory_contributions_contributed_to_that_eps_or_eoc),
                self.convert_str(total_additional_upc_value_contributed_to_that_eps_or_eoc),
                self.convert_str(net_value_contributions_quote),
                self.convert_str(number_of_days_past_due_settled),
                self.convert_str(value_interest_on_arrears_mandatory_contributions),
                self.convert_str(value_of_additional_interest_on_arrears_upc),
                self.convert_str(subtotal_contributions_contribution),
                self.convert_str(subtotal_additional_upc_contributions),
                self.convert_str(total_to_pay_for_mandatory_quotation),
                self.convert_str(total_to_pay_for_additional_upc),
                self.convert_str(total_to_be_paid_to_the_administrator),
                self.convert_str(total_affiliates_by_eps_or_eoc),
                ]
          #VALIDACIÓN
          print("lineas nominas REGISTRO TIPO 5. TOTAL APORTES DEL PERÍODO PARA SALUD")
          pos_i = 1
          pos_f = 1
          for i in lines_detail_register_eps[int(code)+orden]:
              pos_f = pos_i + len(i) -1
              print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
              pos_i = pos_f+1


               

        for x in lines_detail_register_eps:
            elements = [
                lines_detail_register_eps[x][0],
                lines_detail_register_eps[x][1],
                lines_detail_register_eps[x][2],
                lines_detail_register_eps[x][3],
                lines_detail_register_eps[x][4],
                lines_detail_register_eps[x][5],
                lines_detail_register_eps[x][6],
                lines_detail_register_eps[x][7],
                lines_detail_register_eps[x][8],
                lines_detail_register_eps[x][9],
                lines_detail_register_eps[x][10],
                lines_detail_register_eps[x][11],
                lines_detail_register_eps[x][12],
                lines_detail_register_eps[x][13],
                lines_detail_register_eps[x][14],
                lines_detail_register_eps[x][15],
                lines_detail_register_eps[x][16],
            ]
            res.append(''.join(elements))


      #REGISTRO TIPO 6. TOTAL APORTES DEL PERÍODO PARA RIESGOS LABORALES 

        list_unique_arl = list(dict.fromkeys(list_arl))
        sequence = 0
        for arl in list_unique_arl:
          orden += 1
          sequence += 1
          type_of_register = self.white_spaces('06',2,'left','0')
          number_sequence = self.white_spaces(sequence,5,'left','0')
          code_arl = self.white_spaces(self.code_arl(arl,self.payslip_run_id),6,'right',' ')
          nit_de_la_arl = self.white_spaces(self.nit_de_la_arl(arl,self.payslip_run_id),16,'right',' ')
          arl_check_digit = self.white_spaces(self.arl_check_digit(arl,self.payslip_run_id),1,'left','0')
          total_value_of_contributions_reported_to_that_manager = self.white_spaces(self.total_value_of_contributions_reported_to_that_manager(arl,self.payslip_run_id),13,'left','0')
          authorization_number_for_disability_payments = self.white_spaces('',15,'right',' ')
          total_value_of_disabilities_paid = self.white_spaces('',13,'left','0')
          value_of_contributions_paid_to_other_systems = self.white_spaces('',13,'left','0')
          net_value_contributions_quote = self.white_spaces(self.total_value_of_contributions_reported_to_that_manager(arl,self.payslip_run_id),13,'left','0')
          number_of_days_past_due_settled = self.white_spaces('',4,'left','0')
          interest_value_overdue_on_mandatory_contributions = self.white_spaces('',11,'left','0')
          subtotal_contributions_contribution = self.white_spaces(self.total_value_of_contributions_reported_to_that_manager(arl,self.payslip_run_id),13,'left','0')
          unique_form_number_or_initial_integrated_return_object_of_balance_in_favor_of_the_employer = self.white_spaces('',10,'left','0')
          balance_value_in_favor_of_the_previous_period = self.white_spaces('',11,'left','0')
          total_to_be_paid_to_the_administrator = self.white_spaces(self.total_value_of_contributions_reported_to_that_manager(arl,self.payslip_run_id),13,'left','0')
          occupational_risk_fund = self.white_spaces(int(round(self.total_value_of_contributions_reported_to_that_manager(arl,self.payslip_run_id)/100,2)),11,'left','0')
          total_affiliates_per_manager = self.white_spaces(self.total_affiliates_per_manager(arl,self.payslip_run_id),8,'left','0')


          code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
          
          lines_detail_register_arl[int(code)+orden] = [
                self.convert_str(type_of_register),
                self.convert_str(number_sequence),
                self.convert_str(code_arl),
                self.convert_str(nit_de_la_arl),
                self.convert_str(arl_check_digit),
                self.convert_str(total_value_of_contributions_reported_to_that_manager),
                self.convert_str(authorization_number_for_disability_payments),
                self.convert_str(total_value_of_disabilities_paid),
                self.convert_str(value_of_contributions_paid_to_other_systems),
                self.convert_str(net_value_contributions_quote),
                self.convert_str(number_of_days_past_due_settled),
                self.convert_str(interest_value_overdue_on_mandatory_contributions),
                self.convert_str(subtotal_contributions_contribution),
                self.convert_str(unique_form_number_or_initial_integrated_return_object_of_balance_in_favor_of_the_employer),
                self.convert_str(balance_value_in_favor_of_the_previous_period),
                self.convert_str(total_to_be_paid_to_the_administrator),
                self.convert_str(occupational_risk_fund),
                self.convert_str(total_affiliates_per_manager),

                ]
          #VALIDACIÓN
          print("lineas nominas REGISTRO TIPO 6. TOTAL APORTES DEL PERÍODO PARA RIESGOS LABORALES")
          pos_i = 1
          pos_f = 1
          for i in lines_detail_register_arl[int(code)+orden]:
              pos_f = pos_i + len(i) -1
              print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
              pos_i = pos_f+1


        for x in lines_detail_register_arl:
            elements = [
                lines_detail_register_arl[x][0],
                lines_detail_register_arl[x][1],
                lines_detail_register_arl[x][2],
                lines_detail_register_arl[x][3],
                lines_detail_register_arl[x][4],
                lines_detail_register_arl[x][5],
                lines_detail_register_arl[x][6],
                lines_detail_register_arl[x][7],
                lines_detail_register_arl[x][8],
                lines_detail_register_arl[x][9],
                lines_detail_register_arl[x][10],
                lines_detail_register_arl[x][11],
                lines_detail_register_arl[x][12],
                lines_detail_register_arl[x][13],
                lines_detail_register_arl[x][14],
                lines_detail_register_arl[x][15],
                lines_detail_register_arl[x][16],
                lines_detail_register_arl[x][17],
            ]
            res.append(''.join(elements))

        #REGISTRO TIPO 7. TOTAL APORTES DEL PERÍODO PARA CAJAS DE COMPENSACIÓN FAMILIAR  

        list_unique_ccf = list(dict.fromkeys(list_ccf))
        print("list_unique_ccf ", list_unique_ccf)
        print("orden ", orden)
        sequence = 0
        for ccf in list_unique_ccf:
          orden += 1
          sequence += 1
          type_of_register = self.white_spaces('07',2,'left','0')
          number_sequence = self.white_spaces(sequence,5,'left','0')
          ccf_code = self.white_spaces(self.ccf_code(ccf,self.payslip_run_id),6,'right',' ')
          compulsory_identification_number_nit_of_the_ccf = self.white_spaces(self.compulsory_identification_number_nit_of_the_ccf(ccf,self.payslip_run_id),16,'right',' ')
          ccf_check_digit = self.white_spaces(self.ccf_check_digit(ccf,self.payslip_run_id),1,'left','0')
          value_contribution_to_that_ccf = self.white_spaces(self.value_contribution_to_that_ccf(ccf,self.payslip_run_id),13,'left','0')
          number_of_days_past_due_settled = self.white_spaces('',4,'left','0')
          value_of_default_interest_on_the_contribution = self.white_spaces('',11,'left','0')
          total_to_pay_to_the_ccf = self.white_spaces(self.value_contribution_to_that_ccf(ccf,self.payslip_run_id),13,'left','0')
          total_affiliates_per_ccf = self.white_spaces(self.total_affiliates_per_ccf(ccf,self.payslip_run_id),8,'left','0')

          code = self.convert_str(payslip.id)+self.convert_str(payslip.employee_id.identification_id)
          
          lines_detail_register_ccf[int(code)+orden] = [
                self.convert_str(type_of_register),
                self.convert_str(number_sequence),
                self.convert_str(ccf_code),
                self.convert_str(compulsory_identification_number_nit_of_the_ccf),
                self.convert_str(ccf_check_digit),
                self.convert_str(value_contribution_to_that_ccf),
                self.convert_str(number_of_days_past_due_settled),
                self.convert_str(value_of_default_interest_on_the_contribution),
                self.convert_str(total_to_pay_to_the_ccf),
                self.convert_str(total_affiliates_per_ccf),
                ]
          #VALIDACIÓN
          print("lineas nominas REGISTRO TIPO 7. TOTAL APORTES DEL PERÍODO PARA CAJAS DE COMPENSACIÓN FAMILIAR  ")
          pos_i = 1
          pos_f = 1
          for i in lines_detail_register_ccf[int(code)+orden]:
              pos_f = pos_i + len(i) -1
              print(self.white_spaces(len(i),4,'right',' ')+'['+str(pos_i)+'-'+str(pos_f)+']'+'  '+i)
              pos_i = pos_f+1


        for x in lines_detail_register_ccf:
            elements = [
                lines_detail_register_ccf[x][0],
                lines_detail_register_ccf[x][1],
                lines_detail_register_ccf[x][2],
                lines_detail_register_ccf[x][3],
                lines_detail_register_ccf[x][4],
                lines_detail_register_ccf[x][5],
                lines_detail_register_ccf[x][6],
                lines_detail_register_ccf[x][7],
                lines_detail_register_ccf[x][8],
                lines_detail_register_ccf[x][9],
            ]
            print(elements)
            res.append(''.join(elements))

        for i in res:
          self.delete_tildes(i)

        return res


    
    def estruct18(self):
        res = []
        for payslips in self.payslip_run_id:
            for payslip in payslips.slip_ids:
                for concept in payslip.line_ids:
                    #print('APARECE EN NOMINA: ',concept.appears_on_payslip)
                    #print('salary_rule_id: ',concept.salary_rule_id)
                    #print('table_22_id: ',concept.salary_rule_id.table_22_id)
                    if concept.appears_on_payslip and concept.salary_rule_id.table_22_id:
                        elements = [
                            self.convert_str(payslip.employee_id.type_document_id.name),
                            self.convert_str(payslip.employee_id.identification_id),
                            '0'+concept.salary_rule_id.table_22_id.code if len(concept.salary_rule_id.table_22_id.code)<4 else concept.salary_rule_id.table_22_id.code,
                            self.convert_amount(concept.total),
                            self.convert_amount(concept.total),
                            ''
                        ]
                        res.append('|'.join(elements))
        return res

