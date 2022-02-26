# -- coding: utf-8 --
from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


def year_now():
    return datetime.now().year

YEAR_SELECTION = [(str(year), year) for year in range(1935, year_now()+1)]


class HRBondFamily(models.Model): 
    _name = 'hr.bond.family'
    _description = 'table bond family'

    name = fields.Char('Vinculo Familiar')

class HRTypePayment(models.Model):
    _name = 'hr.type.payment'
    _description = 'table type payment'

    name= fields.Char(string='Tipo de Pago')

class HRReasonTermination(models.Model):
    _name = 'hr.reason.termination'
    _description = 'table reason termination'

    name = fields.Char('Motivo de Cese')

class HRSpecialSituation(models.Model): 
    _name = 'hr.special.situation'
    _description = 'Situación Especial'

    name = fields.Char(string='Situacion Especial')


class HRTypeEmployee(models.Model):
    _name = 'hr.type.employee'
    _description = 'Tipo de Trabajador'

    name = fields.Char(string='Tipo de Trabajador')
class HRNit(models.Model):
    _name = 'hr.nit'
    _description = 'NIT'
    
    name = fields.Char(string='NIT')
    code = fields.Char(string='Dígito de verificación')

class HRPensionFund(models.Model):
    _name = 'hr.pension.fund'
    _description = 'AFP'

    name = fields.Char(string='AFP')
    percentage_incoming_required = fields.Float('% de aporte obligatorio')
    commission_on_flow = fields.Float('Comisión sobre flujo')
    commission_on_flow_mix = fields.Float('Comisión sobre flujo - Mixta')
    sure_prime = fields.Float('Prima de Seguros')
    maximum_insurable_remuneration = fields.Float('Remuneración máxima asegurable')

    code = fields.Char('Código')
    
    contact_id = fields.Many2one(comodel_name='res.partner',string='Empresa')
    nit = fields.Char(related='contact_id.vat',string='NIT')
    country_id = fields.Many2one('res.country','País')

    company_ids = fields.Many2many('res.company','x_hr_pension_fund_res_company_rel','pension_fund_id',string="Compañia Permitida")

class HRFamily(models.Model):
    _name = 'hr.family'
    _description = 'Familiares del Trabajador'

    #Datos Familiares
    hr_employee_id = fields.Many2one('hr.employee', string='Empleado')
    names_surnames_family = fields.Char('Nombres y Apellidos')
    bond_family = fields.Many2one('hr.bond.family', string='Vinculo Familiar')
    birthdate_family = fields.Date(string='Fecha de Nacimiento')
    type_document_id = fields.Many2one('l10n_latam.identification.type', 
        string="Tipo de Documento Identificacion")
    doc_number = fields.Char('Numero de Documento')


class HROtherIncome(models.Model):
    _name = 'hr.other.income'
    _description = 'table other income'
    #Ext_ingreso
    hr_employee_id = fields.Many2one('hr.employee', string='Empleado')
    period_id = fields.Many2one('hr.payroll.period',string='Periodo Afecta')
    total_received = fields.Float('Total Percibido')
    total_withheld = fields.Float('Total Retenido') 
    
    def write(self, vals):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        if 'period_id' in vals:
            if not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede modificar este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(hr_other_income, self).write(vals)

    def unlink(self):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        return super(hr_other_income, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'period_id' in vals and not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede crear este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(hr_other_income, self).create(vals_list)


class HRSede(models.Model):
    _name = 'hr.sede'
    _description = 'Sede'

    name = fields.Char('Sede')

class HRArea(models.Model):
    _name = 'hr.area'
    _description = 'Area'

    name = fields.Char('Area')

class HRSeccion(models.Model):
    _name = 'hr.seccion'
    _description = 'seccion'

    name = fields.Char('Seccion')

class HRTurno(models.Model):
    _name = 'hr.turno'
    _description = 'turno'

    name = fields.Char('Turno')

class HRCooperative(models.Model):
    _name = 'hr.cooperative'
    _description = 'cooperativa'

    name = fields.Char('Cooperativa')


class HROccupational_group(models.Model):
    _name = 'hr.occupational.group'
    _description = 'cooperativa'

    name = fields.Char('Cooperativa')

class HRInstruction_grade(models.Model):
    _name = 'hr.instruction.grade'
    _description = 'Instruccion'

    name = fields.Char('Instruccion')

class HRCatRem(models.Model):
    _name = 'hr.cat.rem'
    _description = 'Categoria Remunerativa'

    name = fields.Char('Categoría')

class HRCatEmployee(models.Model):
    _name = 'hr.cat.employee'
    _description = 'Categoria Trabajador'

    name = fields.Char('Categoría')    

class ResBank(models.Model):
    _inherit = "res.bank"

    code = fields.Char('Código')

class AccountType(models.Model):
    _name = 'account.type'

    name = fields.Char('Tipo de Cuenta')
    code = fields.Char('Código')
    bank_id = fields.Many2one('res.bank', string='Banco')
    code_bank = fields.Char(string='Codigo Banco',related='bank_id.code')
     
     
class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    acc_type_bank = fields.Many2one('account.type', string="Tipo de Cuenta")

    currency_id = fields.Many2one('res.currency','Moneda')

class L10nLatamIdentificationType(models.Model):
    _inherit = "l10n_latam.identification.type"

    code = fields.Char('Código')



class employee(models.Model):
    _inherit = "hr.employee"

    code = fields.Char('Codigo')
    last_name = fields.Char('Apellido Paterno')
    mother_last_name = fields.Char('Apellido Materno')
    names = fields.Char('Nombres')
  
    #Información privada

    #COLOMBIA
    type_transport_id = fields.Many2one('hr.type.transport', string="Medio de transporte")
    document_issue_date = fields.Date(string='Fecha Expedición Documento')
    #COLOMBIA
    

    #Datos Personales
    type_document_id = fields.Many2one(related='address_home_id.l10n_latam_identification_type_id', 
        string="Tipo de Documento Identificacion")

    identification_id = fields.Char(related='address_home_id.vat', 
        string="Tipo de Documento Identificacion")

    #COLOMBIA

    eps_id = fields.Many2one('hr.eps', string="EPS")
    ccf_id = fields.Many2one('hr.ccf', string="CCF")
    layoffs_id = fields.Many2one('hr.type.layoffs', string="Cesantías")
    #COLOMBIA
    
    pension_fund = fields.Many2one('hr.pension.fund', string='AFP')
    code_cussp = fields.Char('Codigo CUSSP')
    date_enrollment_afp = fields.Date('Fecha de Inscripcion AFP')
    commission_scheme = fields.Selection(
        string="Esquema de Comision",
        selection=[
            ('mixta', 'Mixta'),
            ('flujo', 'Flujo'),
        ], default="mixta"
    )
    detailed_address = fields.Char('Domicilio Detallado')

    #Adicional
    not_consider_calculation = fields.Boolean('No considerar en el Calculo', default=False)
    no_declarar_al_pdt = fields.Boolean('No declarar al PDT', default=False)
    no_affection_fifth = fields.Boolean('No afecto a Quinta', default=False)

    #Datos Laborales

    date_entry = fields.Date('Fecha de Ingreso')
    type_employee = fields.Many2one(string='Tipo Trabajador', comodel_name='hr.type.employee')
    affiliate_eps= fields.Boolean('Afiliado a EPS?', default=False)
    date_termination = fields.Date('Fecha de Cese')
    reason_termination = fields.Many2one(string='Motivo de Cese', comodel_name='hr.reason.termination')
    obsv_termination = fields.Char('Observación Cese')
    assignment_family = fields.Boolean('Asignacion Familiar?', default=False)
    #COLOMBIA
    type_contributor_id = fields.Many2one(string='Tipo de Cotizante', comodel_name='hr.type.contributor')
    type_risk_arl_id = fields.Many2one(string='Riesgo ARL', comodel_name='hr.type.risk.arl')
    arl_id = fields.Many2one(string='ARL', comodel_name='hr.arl')
    reason_work_suspension_id = fields.Many2one(string='Motivo Suspensión Laboral', comodel_name='hr.reason.work.suspension')

    #COLOMBIA

    account_bank_principal = fields.Many2one('res.partner.bank','Cuenta Bancaria Principal')
    account_bank_cts = fields.Many2one('res.partner.bank','Cuenta Bancaria CTS')


    #Informacion Fiscal

    income_declarant = fields.Boolean(string="Declarante de Renta")
    beneficiaries = fields.Boolean(string="Beneficiarios")
    monetary_correction_relief = fields.Float(string="Alivio Correccion Monetaria")
    prepaid_medicine_relief = fields.Float(string="Alivio Medicina Prepagada")
    withholding_procedure = fields.Many2one(string='Procedimiento de Retencion', comodel_name='hr.withholding.procedure')
    porcent_retention_pr2 = fields.Float('%  de retencion PR2')

    #Datos Complementarios
    special_situation = fields.Many2one(string='Situacion Especial', comodel_name='hr.special.situation')
    type_payment = fields.Many2one(string='Tipo de Pago', comodel_name='hr.type.payment')

    #Datos Familiares
    family_ids = fields.One2many('hr.family','hr_employee_id',string="Familia")

    #Otros ingresos de quinta Categoria
    other_income_ids = fields.One2many('hr.other.income','hr_employee_id', string="Otros ingresos ")

    sede_id = fields.Many2one('hr.sede','Sede')
    area_id = fields.Many2one('hr.area','Area')
    seccion_id = fields.Many2one('hr.seccion','Seccion')
    turn_id = fields.Many2one('hr.turno','Turno')
    cooperative_id = fields.Many2one('hr.cooperative','Cooperativa')
    salaries_per_year = fields.Char('Nº Sueldos por Año')
    occupational_group_id = fields.Many2one('hr.occupational.group','Grupo Ocupacional')
    #mobile_work = fields.Char(string='Móvil del trabajo')

    spouse_date_marital = fields.Date('Fecha de Matrimonio')
    group_blood = fields.Selection([
        ('O-','O-'),('O+','O+'),('A−','A-'),('A+','A+'),('B−','B-'),('B+','B+'),('AB−','AB−'),('AB+','AB+') 
        ],'Grupo Sanguineo')

    country_of_resd = fields.Many2one('res.country','País de Residencia')
    phone2 = fields.Char('Teléfono 2')
    phone3 = fields.Char('Teléfono 3')
    private_email2 = fields.Char('Correo electrónico 2')
    type_house = fields.Char('Tipo de Casa')

    type_instruction_grade_id = fields.Many2one('hr.instruction.grade','Tipo de Instrucción')
    cat_rem_id = fields.Many2one('hr.cat.rem','Categoría Remunerativa')
    cat_employee_id = fields.Many2one('hr.cat.employee','Categoría del Trabajador')
    
    forma_de_ingreso = fields.Char('Forma de Ingreso')
    anexo = fields.Char('Anexo')
    sindicato = fields.Char('Sindicato') 
    obs_gral = fields.Char('Observación') 
    

    moneda_sueldo = fields.Many2one('res.currency','Moneda')
    sueldo = fields.Float('Sueldo')
    n_hijos_no_dep = fields.Char('Nº de Hijos No Dependientes')
    dias_derecho_vacacional = fields.Integer('Dias de Derecho Vacacional')
    dias_derecho_fisicas = fields.Integer('Dias de Derecho Fisicas')
    tope_compra_vacaciones = fields.Integer('Tope Compra de Vacaciones')


    code_country_company= fields.Char(related="company_id.country_id.code")
    country_company= fields.Many2one('res.country',related="company_id.country_id")

    """
    def name_get(self):
        result = []
        for line in self:
            l_name = line.name
            if line.last_name:
                l_name+=' '+line.last_name
            if line.mother_last_name:
                l_name+=' '+line.mother_last_name
            name = l_name
            result.append((line.id, name))
        return result
    """
    def get_string_marital(self):
        value = ""

        if self.marital == 'single':
            value = "Soltero (a)"

        if self.marital == 'married':
            value = "Casado (a)" 

        if self.marital == 'cohabitant':
            value = "Cohabitante legal"

        if self.marital == 'widower':
            value = "Viudo (a)"

        if self.marital == 'divorced':
            value = "Divorciado"

        return value

    def get_age(self):
        birthDate = self.birthday
        today = fields.date.today() 
        age = birthDate and today.year - birthDate.year -  ((today.month, today.day) <  (birthDate.month, birthDate.day)) or 0
        print(age)
        return age or 0

class contract_inherit(models.Model):
    _inherit = "hr.contract"

    type_risk_arl_id = fields.Many2one(string='Riesgo ARL', comodel_name='hr.type.risk.arl')
    type_contributor_id = fields.Many2one(string='Tipo de Cotizante', comodel_name='hr.type.contributor')
    subtype_contributor_id = fields.Many2one(string='Subtipo de Cotizante', comodel_name='hr.subtype.contributor')
    foreigner_not_obliged_to_contribute_to_pensions = fields.Boolean(string='Extranjero no obligado a cotizar a pensiones', default=False)
    colombian_abroad = fields.Boolean(string='Colombiano en el exterior', default=False)
    type_employee = fields.Many2one(string='Tipo Trabajador', comodel_name='hr.type.employee')

    code_country_company = fields.Char(related="company_id.country_id.code")
    #COLOMBIA

class HRArl(models.Model):
    _name = 'hr.arl'
    _description = 'ARL - Administradora de Riesgos Laborales'

    name = fields.Char('Nombre')
    code = fields.Char('Código')
    contact_id = fields.Many2one(comodel_name='res.partner',string='Empresa')
    nit = fields.Char(related='contact_id.vat',string='NIT')
    country_id = fields.Many2one('res.country','País')

    company_ids = fields.Many2many('res.company','x_hr_arl_res_company_rel','arl_id',string="Compañia Permitida")

class hrTypeTransport(models.Model):
    _name = 'hr.type.transport'
    _description = 'Medio de transporte'

    name = fields.Char('Medio de transporte')

    company_ids = fields.Many2many('res.company','x_hr_type_transport_company_rel','type_transport_id',string="Compañia Permitida")

class hrTypeLayoffs(models.Model):
    _name = 'hr.type.layoffs'
    _description = 'Tipo de cesantías'

    name = fields.Char('Tipo de cesantías')

    contact_id = fields.Many2one(comodel_name='res.partner',string='Empresa')
    nit = fields.Char(related='contact_id.vat',string='NIT')

    company_ids = fields.Many2many('res.company','x_hr_type_layoffs_company_rel','type_layoffs_id',string="Compañia Permitida")

class hrTypeContributor(models.Model):
    _name = 'hr.type.contributor'
    _description = 'Tipo de cotizante'

    name = fields.Char('Tipo de cotizante')
    code = fields.Char('Código')
    country_id = fields.Many2one('res.country','País')

    company_ids = fields.Many2many('res.company','x_hr_type_contributor_company_rel','type_contributor_id',string="Compañia Permitida")

class HRSubtypeContributor(models.Model):
    _name = "hr.subtype.contributor"
    _description = 'Subtipo de Cotizante'

    name = fields.Char('Subtipo de Cotizante')
    code = fields.Char('Código')
    country_id = fields.Many2one('res.country','País')

    company_ids = fields.Many2many('res.company','x_hr_subtype_contributor_company_rel','subtype_contributor_id',string="Compañia Permitida")

class hrTypeRiskARL(models.Model):
    _name = 'hr.type.risk.arl'
    _description = 'Tipo de riesgo ARL'

    name = fields.Float('Tipo de riesgo ARL',digits=(12,3))
    code = fields.Char('Código')

    company_ids = fields.Many2many('res.company','x_hr_type_risk_arl_company_rel','type_risk_arl_id',string="Compañia Permitida")

class hrWithholdingProcedure(models.Model):
    _name = 'hr.withholding.procedure'
    _description = 'Tipo de procedimiento de retencion'

    name = fields.Char('Tipo de procedimiento de retencion')

    company_ids = fields.Many2many('res.company','x_hr_withholding_procedure_company_rel','withholding_procedure_id',string="Compañia Permitida")

class HRHealthPromotionEntity(models.Model):
    _name = 'hr.eps'
    _description = 'Entidad Promotora de Salud'

    name = fields.Char(string='EPS')
    code = fields.Char(string='Código')

    contact_id = fields.Many2one(comodel_name='res.partner',string='Empresa')
    nit = fields.Char(related='contact_id.vat',string='NIT')
    country_id = fields.Many2one(comodel_name='res.country', string='País')

    company_ids = fields.Many2many('res.company','x_hr_eps_company_rel','eps_id',string="Compañia Permitida")


class HRFamilyCompensationFund(models.Model):
    _name = 'hr.ccf'
    _description = 'Caja de Compensación Familiar'

    name = fields.Char(string='CCF')
    code = fields.Char(string='Código')
    contact_id = fields.Many2one(comodel_name='res.partner',string='Empresa')
    nit = fields.Char(related='contact_id.vat',string='NIT')
    country_id = fields.Many2one(comodel_name='res.country', string='País')

    company_ids = fields.Many2many('res.company','x_hr_ccf_company_rel','ccf_id',string="Compañia Permitida")


class HRReasonWorkSuspension(models.Model):
    _name = 'hr.reason.work.suspension'
    _description = 'Motivo Suspensión Laboral'
    name = fields.Char(string='Motivo Suspensión Laboral')


class HRCountryDepartment(models.Model):
    _description = "Departamento"
    _name = 'hr.country.department'

    
    name = fields.Char(string='Departamento')
    code = fields.Char(string='Code')
    country_id = fields.Many2one('res.country', string='Country')

class HRResCity(models.Model):
    _description = "Ciudad"
    _inherit = 'res.city'

    code = fields.Char(string='Code')
    department_id = fields.Many2one(comodel_name='hr.country.department', string='Departamento')




"""
class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'
    
    company_ids = fields.Many2many('res.company','x_iruimenu_res_company_rel','iruimenu_id',string="Compañia Permitida")
"""
