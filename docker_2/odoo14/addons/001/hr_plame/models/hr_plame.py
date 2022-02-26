# -*- coding: utf-8 -*-
##############################################################################

from odoo import api, fields, models
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    table_22_id = fields.Many2one(comodel_name='hr.table.22',
                                  string="Tabla 22 SUNAT",
                                  required=False)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'


    def _get_payslip_lines(self):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = localdict['categories'].dict.get(category.code, 0) + amount
            return localdict

        self.ensure_one()
        result = {}
        rules_dict = {}
        worked_days_dict = {line.code: line for line in self.worked_days_line_ids if line.code}
        inputs_dict = {line.code: line for line in self.input_line_ids if line.code}

        employee = self.employee_id
        contract = self.contract_id

        localdict = {
            **self._get_base_local_dict(),
            **{
                'categories': BrowsableObject(employee.id, {}, self.env),
                'rules': BrowsableObject(employee.id, rules_dict, self.env),
                'payslip': Payslips(employee.id, self, self.env),
                'worked_days': WorkedDays(employee.id, worked_days_dict, self.env),
                'inputs': InputLine(employee.id, inputs_dict, self.env),
                'employee': employee,
                'contract': contract
            }
        }
        imp_essalud=0
        imp_spp=0
        imp_onp=0
        imp_5ta=0
        for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
            localdict.update({
                'result': None,
                'result_qty': 1.0,
                'result_rate': 100})
            if rule._satisfy_condition(localdict):
                amount, qty, rate = rule._compute_rule(localdict)
                #check if there is already a rule computed with that code
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                #set/overwrite the amount computed for this rule in the localdict
                tot_rule = amount * qty * rate / 100.0
                if rule.table_22_id:
                    if rule.table_22_id.essalud_assured_employee:
                        imp_essalud += tot_rule
                    if rule.table_22_id.fund_19990:
                        imp_onp += tot_rule
                    if rule.table_22_id.fund_spp:
                        imp_spp += tot_rule
                    if rule.table_22_id.income_tax_5ta:
                        imp_5ta += tot_rule
                localdict['imp_essalud'] = imp_essalud
                localdict['imp_spp'] = imp_spp
                localdict['imp_onp'] = imp_onp
                localdict['imp_5ta'] = imp_5ta
                localdict[rule.code] = tot_rule
                rules_dict[rule.code] = rule
                # sum the amount for its salary category
                localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                # create/overwrite the rule in the temporary results
                result[rule.code] = {
                    'sequence': rule.sequence,
                    'code': rule.code,
                    'name': rule.name,
                    'note': rule.note,
                    'salary_rule_id': rule.id,
                    'contract_id': contract.id,
                    'employee_id': employee.id,
                    'amount': amount,
                    'quantity': qty,
                    'rate': rate,
                    'slip_id': self.id,
                }
        return result.values()


class hr_table_22_category(models.Model):
    _name = 'hr.table.22.category'
    _description = 'Categorias de Ingresos,tributos y descuentos'

    name = fields.Char(string='Descripción')
    code = fields.Char(string='Código', size=4)

class hr_table_22(models.Model):
    _name = 'hr.table.22'
    _description = 'Ingresos,tributos y descuentos'

    name = fields.Char(string='Descripción')
    code = fields.Char(string='Código', size=4)
    category_id = fields.Many2one(comodel_name='hr.table.22.category', string='Categoría')
    essalud_assured_employee = fields.Boolean(string='ESSALUD Seguro regular trabajador')
    essalud_assured_fishing = fields.Boolean(string='ESSALUD Seguro regular trabajador Pesquero')
    essalud_assured_agrarian = fields.Boolean(string='ESSALUD Seguro Agrario/Acuicultor')
    essalud_sctr = fields.Boolean(string='ESSALUD SCTR')
    extraordinary_solidarity_tax = fields.Boolean(string='Impuesto Extraordinario de Solidaridad')
    fund_artist = fields.Boolean(string='Fondo Derechos Sociales del Artista')
    senati = fields.Boolean(string='SENATI')
    fund_19990 = fields.Boolean(string='Sistema Nacional de Pensiones 19990')
    fund_spp = fields.Boolean(string='Sistema Privado de Pensiones')
    fund_min = fields.Boolean(string='Fondo Compl de Jubil Min, Met Y Sider')
    fund_fishing = fields.Boolean(string='Rég.Esp. Pensiones   Trab. Pesquero')
    income_tax_5ta = fields.Boolean(string='Renta 5ta Categoria Retenciones')
    essalud_regular = fields.Boolean(string='ESSALUD Seguro Regular Pensionista')
    solidarity_contribution = fields.Boolean(string='Contribución Solidaria Asistencia Previs.')
