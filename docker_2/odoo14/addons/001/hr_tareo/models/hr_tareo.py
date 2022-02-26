# -*- coding: utf-8 -*-
##############################################################################

from datetime import datetime, timedelta
from pytz import timezone, UTC
from dateutil.rrule import DAILY, rrule
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class hr_tareo(models.Model):
    _name = 'hr.tareo'
    _description = 'Department Novedades'
    name = fields.Char(compute='_compute_name', string='Descripción', size=64,
                       required=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    detail_ids = fields.One2many(
        comodel_name='hr.tareo.detail', inverse_name='tareo_id',
        string='Detalle del Novedades', readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('country_id.code','=','PE')]")

    detail_co_ids = fields.One2many(
        comodel_name='hr.tareo.detail', inverse_name='tareo_id',
        string='Detalle del Novedades', readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('country_id.code','=','CO')]")


    period_id = fields.Many2one(comodel_name='hr.payroll.period',
                                string='Periodo', required=True)
    country_id = fields.Many2one('res.country','País',
        default=lambda self:self.env.company.country_id.id)
    code_country = fields.Char('Código País', related="country_id.code")
    date_start = fields.Date(
        string='Fecha de inicio', related='period_id.date_start', readonly=1)
    date_end = fields.Date(
        string='Fecha de fin', related='period_id.date_end', readonly=1)
    state = fields.Selection((('draft', 'Borrador'),
                              ('validate', 'Confirmado')), string='Estado',
                             required=True, readonly=True,
                             default='draft')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True, index=True, readonly=True)


    '''_sql_constraints = [
        ('name_unique', 'unique(name), company_id', 'El nombre de las Novedades debe ser único por compañía'),
    ]'''

    def action_validate(self):
        for tareo in self:
            tareo.write({'state':'validate'})
    
    @api.depends('period_id')
    def _compute_name(self):
        for tareo in self:
            tareo.name = "Novedades " + "%s" % (tareo.period_id and tareo.period_id.name or '')

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

    @api.model
    def create_details(self, tareo):
        employees = self.env['hr.employee'].search([('company_id', '=', self.env.company.id)])
        print(self.env.company.id)
        sequence = 0
        for employee in employees:
            contract_ids = employee._get_contracts(tareo.date_start, tareo.date_end)
            sequence +=1
            if contract_ids:
                val = {
                    'sequence': self.white_spaces(sequence,3,'left','0'),
                    'employee_id': employee.id,
                    'tareo_id': tareo.id,
                    #'country_id': employee.company_id.country_id.id
                }

                for key, value in val.items():
                    print (key, 'value', value)
                print(val)
                self.env['hr.tareo.detail'].create(val)
        return True

    def create_details_recharge(self, tareo):

        tareo_details = self.env['hr.tareo.detail'].search([('tareo_id', '=', self.id)])
        list_employees_existing_ids = []
        for tareo_detail in tareo_details:
            list_employees_existing_ids.append(tareo_detail.employee_id.id)

        
        employees = self.env['hr.employee'].search([('company_id', '=', self.env.company.id),('id', 'not in', list_employees_existing_ids)])
        print(self.env.company.id)
        for employee in employees:
            contract_ids = employee._get_contracts(tareo.date_start, tareo.date_end)
            if contract_ids:
                val = {
                    'employee_id': employee.id,
                    'tareo_id': tareo.id,
                    #'country_id': employee.company_id.country_id.id
                }

                for key, value in val.items():
                    print (key, 'value', value)
                print(val)
                self.env['hr.tareo.detail'].create(val)

        tareo_details_total = self.env['hr.tareo.detail'].search([('tareo_id', '=', self.id)])
        sequence = 0
        for tareo_detail in tareo_details_total:
            sequence += 1
            tareo_detail.sequence = self.white_spaces(sequence,3,'left','0')
        
        return True

    @api.model
    def create(self, vals):
        list_tareos_existing_id = []
        for tareo in self.env['hr.tareo'].search([]):
            list_tareos_existing_id.append(tareo.period_id.id)
        
        if 'period_id' in vals and not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
            raise ValidationError('No se puede crear este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')

        if vals['period_id'] in list_tareos_existing_id:
            raise ValidationError('Intenta crear una Novedad con un periodo existente en el modelo')
        else:
            my_id = super(hr_tareo, self).create(vals)
            self.create_details(my_id)
        return my_id


    def unlink(self):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        children = self.mapped('detail_ids')
        if children:
            children.unlink()
        return super(hr_tareo, self).unlink()


    def write(self, vals):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        if 'period_id' in vals:
            if not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede modificar este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(hr_tareo, self).write(vals)

    def recharge_tareo(self):
        self.create_details_recharge(self)


class hr_tareo_detail(models.Model):
    _name = 'hr.tareo.detail'
    _description = 'Tareo Detail'


    tareo_id = fields.Many2one(comodel_name='hr.tareo', string='Novedades',
                               required=True)
    company_id = fields.Many2one('res.company','Compañia', related="tareo_id.company_id")
    country_id = fields.Many2one('res.country','País', related="tareo_id.country_id")
    code_country = fields.Char('Código País', related="country_id.code")

    employee_id = fields.Many2one(comodel_name='hr.employee', string='Empleado',
                                  required=True)
    doc_number = fields.Char(string='Documento de Identidad', related='employee_id.identification_id')
    
    #GENERA
    planned_days = fields.Integer(compute='_get_planned_days',
                                  string='Días planeados')
    worked_days = fields.Integer(string='Días trabajados',compute='_get_worked_days')
    state = fields.Selection(selection=(('draft', 'Draft'),
                                        ('validate', 'Confirmed')),
                             string='Estado', required=True, readonly=True,
                             default='draft')

    sequence = fields.Char(String='Secuencia')

    #PERU
    ot25 = fields.Float(string='Horas extras 25', digits=(16, 2))
    ot35 = fields.Float(string='Horas extras 35', digits=(16, 2))
    ot100 = fields.Float(string='Horas extras 100', digits=(16, 2))
    number_leave = fields.Integer(string='N° Faltas')
    hours_of_delay = fields.Integer(string='Minutos de tardanza')
    holidays = fields.Integer(string='N° días vaca.')
    holiday_sale = fields.Integer(string='Días vta. vaca.')
    medical_breaks = fields.Integer(string='Descansos médicos')
    maternity_allowance = fields.Integer(string='Subsidio por Maternidad')
    sickness_allowance = fields.Integer(string='Subsidio por Enfermedad/Accidente')
    license_with_enjoy = fields.Integer(string='Licencia con Goce')
    leave_without_enjoyment = fields.Integer(string='Licencia sin Goce')


    #COLOMBIA
    hed_co = fields.Float(string='Horas Extras Diurna', digits=(16, 2))
    hen_co = fields.Float(string='Horas Extras Nocturnas', digits=(16, 2))
    hefd_co = fields.Float(string='Horas Extras Festivas Diurna', digits=(16, 2))
    hefn_co = fields.Float(string='Horas Extras Festivas Nocturna', digits=(16, 2))
    refe_co = fields.Integer(help='Recargo Festivo')
    reno_co = fields.Integer(help='Recargo Nocturno')
    renf_co = fields.Integer(help='Recargo Nocturno Festivo')
    fesc_co = fields.Integer(help='Festivo Sin Compensatorio')
    ige_co = fields.Integer(help='Incapacidad Enfermedad General', compute='_get_ige')
    irl_co = fields.Integer(help='Incapacidad Accidente Laboral', compute='_get_irl')
    lma_co = fields.Integer(help='Licencia de Maternidad', compute='_get_lma')
    lpa_co = fields.Integer(help='Licencia de Paternidad', compute='_get_lpa')
    vpp_co = fields.Integer(help='Vacaciones prepagadas', compute='_get_vpp')
    vco_co = fields.Integer(help='Vacaciones Compensadas', compute='_get_vco')
    vdi_co = fields.Integer(help='Vacaciones Disfrutadas', compute='_get_vdi')
    vre_co = fields.Integer(help='Vacaciones por Retiro', compute='_get_vre')
    lnr_co = fields.Integer(help='Ausentismo No Remunerado', compute='_get_lnr')
    sln_co = fields.Integer(help='Sancion/ Suspensión', compute='_get_sln')
    lr_co = fields.Integer(help='Licencia Remunerada', compute='_get_lr')
    lt_co = fields.Integer(help='Licencia de Luto', compute='_get_lt')

    
    def _get_vpp(self):
        for line in self:
            if line.employee_id and line.tareo_id.period_id:
                leaves = line.env['hr.leave'].search([('payroll_period_id','=',line.tareo_id.period_id.id),('state','=','validate'),
                    ('holiday_status_id.novelty','=','vdi'),('employee_id','=',line.employee_id.id)])
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.holiday_status_id.days_considered == 'days_business':
                            total += leave.number_of_days
                        else:
                            total += leave.number_of_days_calendar
                line.vpp_co = total


            else:
                line.vpp_co = 0

    def _get_sln(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','sln'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.sln_co = total


            else:
                line.sln_co = 0

    def _get_ige(self):
        #timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        timezone =  'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_init = line.tareo_id.period_id.date_start
                date_end = line.tareo_id.period_id.date_end
                date_start = datetime(date_init.year,date_init.month,date_init.day) + timedelta(hours=-7)
                date_end = datetime(date_end.year,date_end.month,date_end.day)

                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','ige'),('employee_id','=',line.employee_id.id)])
                
                total=0
                for x in leaves:
                    print("JOSE ENTRE IGEEEEEEEEEEE ", x.employee_id.name, x, x.date_from, x.date_to)
                if leaves:
                    for leave in leaves:
                        leave_date_start = datetime(int(leave.request_date_from.year),int(leave.request_date_from.month),int(leave.request_date_from.day))
                        leave_date_end = datetime(int(leave.request_date_to.year),int(leave.request_date_to.month),int(leave.request_date_to.day))
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            print("PRIMER CASO")
                            if leave.holiday_status_id.days_considered == 'days_business':

                                total += leave._get_number_of_days(datetime(2023,12,20), datetime(2024,2,9), False)['days']
                                print("PRIMER CASO ", datetime(2023,12,20), datetime(2024,2,9), leave.employee_id.id)
                                print("PRIMER CASO ", total)
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            print("SEGUNDO CASO")
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            print("TERCER CASO")
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            print("CUARTO CASO")
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.ige_co = total


            else:
                line.ige_co = 0


    def _get_irl(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','irl'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.irl_co = total


            else:
                line.irl_co = 0

    def _get_lma(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','lma'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.lma_co = total


            else:
                line.lma_co = 0

    def _get_lpa(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','lpa'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.lpa_co = total


            else:
                line.lpa_co = 0

    def _get_vco(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','vco'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.vco_co = total


            else:
                line.vco_co = 0

    def _get_vdi(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','vdi'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.vdi_co = total


            else:
                line.vdi_co = 0

    def _get_vre(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','vre'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.vre_co = total


            else:
                line.vre_co = 0

    def _get_lnr(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','lnr'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.lnr_co = total

            else:
                line.lnr_co = 0

    def _get_lr(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','lr'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.lr_co = total


            else:
                line.lr_co = 0

    def _get_lt(self):
        timezone = self._context.get('tz') or self.env.user.partner_id.tz or 'UTC'
        self_tz = self.with_context(tz=timezone)
        for line in self:    
            if line.employee_id and line.tareo_id.period_id:
                date_start = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_start, datetime.max.time()))
                date_end = fields.Datetime.context_timestamp(self_tz, datetime.combine(line.tareo_id.period_id.date_end, datetime.max.time()))
                leaves = line.env['hr.leave'].search([('state','=','validate'),
                    ('holiday_status_id.novelty','=','lt'),('employee_id','=',line.employee_id.id)])
                
                total=0
                
                if leaves:
                    for leave in leaves:
                        if leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_start and leave.request_date_to < line.tareo_id.period_id.date_end:
                            
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, leave.date_to, leave.employee_id.id)['days']
                            else:
                                total += (leave.request_date_to - line.tareo_id.period_id.date_start).days + 1

                        elif leave.request_date_from >= line.tareo_id.period_id.date_start and leave.request_date_to <= line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave.number_of_days
                            else:
                                total += leave.number_of_days_calendar
                        
                        elif leave.request_date_from > line.tareo_id.period_id.date_start and leave.request_date_from < line.tareo_id.period_id.date_end and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(leave.date_from, date_end, leave.employee_id.id)['days']
                            else:
                                total += (line.tareo_id.period_id.date_end - leave.request_date_from).days  
                        elif leave.request_date_from < line.tareo_id.period_id.date_start and leave.request_date_to > line.tareo_id.period_id.date_end:
                            if leave.holiday_status_id.days_considered == 'days_business':
                                total += leave._get_number_of_days(date_start, date_end, leave.employee_id.id)['days']
                            else:
                                total += 30 
                line.lt_co = total


            else:
                line.lt_co = 0


    @api.onchange('employee_id')
    def onchange_employee_validation(self):
        if self.employee_id and self.tareo_id:
            contract = self.employee_id._get_contracts(self.tareo_id.date_start, self.tareo_id.date_end)
            print(contract)
            if not contract.structure_type_id:
                raise UserError('El empleado '+ self.employee_id.name +' no tiene tipo de estructura salarial')

    def _get_planned_days(self):
        for line in self:
            if line.employee_id and line.tareo_id:
                contract = line.employee_id._get_contracts(line.tareo_id.date_start, line.tareo_id.date_end)
                if not contract.structure_type_id:
                    raise UserError('El empleado '+ line.employee_id.name +' no tiene tipo de estructura salarial')
                else:
                    if contract.structure_type_id.default_schedule_pay=='monthly':
                        line.planned_days=30
                    elif contract.structure_type_id.default_schedule_pay=='weekly':
                        line.planned_days=7
            else:
                line.planned_days = 0



    @api.depends('planned_days', 'number_leave', 'medical_breaks','maternity_allowance','sickness_allowance','license_with_enjoy','leave_without_enjoyment', 'holidays',
        'ige_co','irl_co','lma_co','lpa_co','vco_co','lnr_co','sln_co','lr_co','lt_co')
    def _get_worked_days(self):
        for line in self:
            if self.env.ref("base.pe")==line.tareo_id.company_id.country_id:
                if line.planned_days:
                    line.worked_days = line.planned_days - line.number_leave - line.medical_breaks -line.maternity_allowance -line.sickness_allowance -line.license_with_enjoy -line.leave_without_enjoyment -line.holidays
                else:
                    line.worked_days = 0

            if self.env.ref("base.co")==line.tareo_id.company_id.country_id:
                if line.planned_days:
                    line.worked_days = line.planned_days - line.ige_co - line.irl_co -line.lma_co -line.lpa_co -line.vco_co -line.vdi_co -line.vre_co -line.lnr_co -line.sln_co-line.lr_co-line.lt_co
                else:
                    line.worked_days = 0

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    date_start = fields.Date(string='Date Start',
                             related='period_id.date_start',
                             readonly=True)
    date_end = fields.Date(string='Date End', related='period_id.date_end',
                           readonly=True)
    period_id = fields.Many2one(comodel_name='hr.payroll.period',
                                string='Periodo', required=True,
                                states={'draft': [('readonly', False)]})
    move_count = fields.Integer(compute="_get_move_count")

    salary_type = fields.Char(string='Tipo de Nóminas', readonly=True)

    def write(self, vals):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        if 'period_id' in vals:
            if not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede modificar este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(HrPayslipRun, self).write(vals)
    
    def unlink(self):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        return super(HrPayslipRun, self).unlink()
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'period_id' in vals and not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede crear este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(HrPayslipRun, self).create(vals_list)

    def recalculate_slips(self):
        for slip in self.slip_ids:
            slip.action_refresh_from_work_entries()

        payslips = self.env['hr.payslip'].search([('id', 'in', self.slip_ids.ids)])

        for slip in payslips:
            if slip.state == 'verify':
                self.write({'state': 'verify'})
                break
 


    def action_draft_slips(self):
        for slip in self.slip_ids:
            slip.write({'state': 'draft'})

        return self.write({'state': 'draft'})

    

    def cancel_slips(self):
        for slip in self.slip_ids:
            slip.action_payslip_cancel_1()

    def _get_move_count(self):
        for line in self:
            move = self.env['account.move']
            for payslip in line.slip_ids:
                if payslip.move_id not in move:
                    move += payslip.move_id
            line.move_count = len(move)

    def action_open_account_move(self):
        self.ensure_one()
        move = self.env['account.move']
        for payslip in self.slip_ids:
            move += payslip.move_id
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['id', 'in', move.ids]],
            "name": "Asientos Contables",
        }

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    date_from = fields.Date(string='Date Start',
                             related='period_id.date_start',store=True)
    date_to = fields.Date(string='Date End', related='period_id.date_end',store=True)
    period_id = fields.Many2one(comodel_name='hr.payroll.period',
                                string='Periodo', required=True,
                                states={'draft': [('readonly', False)]})

    def action_payslip_cancel_1(self):

        self.write({'state': 'cancel'})
        self.mapped('payslip_run_id').action_close()
        moves = self.mapped('move_id')
        moves.filtered(lambda x: x.state == 'posted').button_cancel()
        moves.unlink()


    def _get_worked_day_lines(self):
        """
        :returns: a list of dict containing the worked days values that should be applied for the given payslip
        """
        res = []
        # fill only if the contract as a working schedule linked
        self.ensure_one()
        contract = self.contract_id
        if contract:
            tareo_id = self.env['hr.tareo'].search([('period_id','=',self.period_id.id),('company_id','=',self.company_id.id)],limit=1).id
            tareo_detail = self.env['hr.tareo.detail'].search([('employee_id','=',contract.employee_id.id),('tareo_id','=',tareo_id)])
            if tareo_detail:

                if self.company_id.country_id.code == 'PE':
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_diat')
                    DIAT = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.worked_days,
                        'number_of_hours': tareo_detail.worked_days*8,
                        'amount': 0,
                    }
                    res.append(DIAT)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_he25')
                    HE25 = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.ot25,
                        'amount': 0,
                    }
                    res.append(HE25)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_he35')
                    HE35 = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.ot35,
                        'amount': 0,
                    }
                    res.append(HE35)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_he10')
                    HE10 = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.ot100,
                        'amount': 0,
                    }
                    res.append(HE10)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_falt')
                    FALT = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.number_leave,
                        'number_of_hours': tareo_detail.number_leave*8,
                        'amount': 0,
                    }
                    res.append(FALT)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_tard')
                    TARD = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.hours_of_delay/60,
                        'amount': 0,
                    }
                    res.append(TARD)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_vaca')
                    VACA = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.holidays,
                        'number_of_hours': tareo_detail.holidays*8,
                        'amount': 0,
                    }
                    res.append(VACA)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_vvac')
                    VVAC = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.holiday_sale,
                        'number_of_hours': tareo_detail.holiday_sale*8,
                        'amount': 0,
                    }
                    res.append(VVAC)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_dmed')
                    DMED = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.medical_breaks,
                        'number_of_hours': tareo_detail.medical_breaks*8,
                        'amount': 0,
                    }
                    res.append(DMED)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_subm')
                    SUBM = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.maternity_allowance,
                        'number_of_hours': tareo_detail.maternity_allowance*8,
                        'amount': 0,
                    }
                    res.append(SUBM)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_sube')
                    SUBE = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.sickness_allowance,
                        'number_of_hours': tareo_detail.sickness_allowance*8,
                        'amount': 0,
                    }
                    res.append(SUBE)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_lcgo')
                    LCGO = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.license_with_enjoy,
                        'number_of_hours': tareo_detail.license_with_enjoy*8,
                        'amount': 0,
                    }
                    res.append(LCGO)
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_csgo')
                    CSGO = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.leave_without_enjoyment,
                        'number_of_hours': tareo_detail.leave_without_enjoyment*8,
                        'amount': 0,
                    }
                    res.append(CSGO)

                elif self.company_id.country_id.code == 'CO':
                #CO  si es mayorq que cero mandar hacer el append() sino no mandarlo 
                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_diat')
                    DIAT = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.worked_days,
                        'number_of_hours': tareo_detail.worked_days*8,
                        'amount': 0,
                    }
                    res.append(DIAT)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_hed')
                    HED = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.hed_co,
                        'amount': 0,
                    }
                    res.append(HED)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_hen')
                    HEN = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.hen_co,
                        'amount': 0,
                    }
                    res.append(HEN)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_hefd')
                    HEFD = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.hefd_co,
                        'amount': 0,
                    }
                    res.append(HEFD)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_hefn')
                    HEFN = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': 0,
                        'number_of_hours': tareo_detail.hefn_co,
                        'amount': 0,
                    }
                    res.append(HEFN)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_refe')
                    REFE = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.refe_co,
                        'number_of_hours': tareo_detail.refe_co*8,
                        'amount': 0,
                    }
                    res.append(REFE)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_reno')
                    RENO = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.reno_co,
                        'number_of_hours': tareo_detail.reno_co*8,
                        'amount': 0,
                    }
                    res.append(RENO)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_renf')
                    RENF = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.renf_co,
                        'number_of_hours': tareo_detail.renf_co*8,
                        'amount': 0,
                    }
                    res.append(RENF)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_fesc')
                    FESC = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.fesc_co,
                        'number_of_hours': tareo_detail.fesc_co*8,
                        'amount': 0,
                    }
                    res.append(FESC)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_ige')
                    IGE = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.ige_co,
                        'number_of_hours': tareo_detail.ige_co*8,
                        'amount': 0,
                    }
                    res.append(IGE)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_irl')
                    IRL = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.irl_co,
                        'number_of_hours': tareo_detail.irl_co*8,
                        'amount': 0,
                    }
                    res.append(IRL)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_lma')
                    LMA = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.lma_co,
                        'number_of_hours': tareo_detail.lma_co*8,
                        'amount': 0,
                    }
                    res.append(LMA)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_lpa')
                    LPA = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.lpa_co,
                        'number_of_hours': tareo_detail.lpa_co*8,
                        'amount': 0,
                    }
                    res.append(LPA)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_vco')
                    VCO = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.vco_co,
                        'number_of_hours': tareo_detail.vco_co*8,
                        'amount': 0,
                    }
                    res.append(VCO)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_vdi')
                    VDI = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.vdi_co,
                        'number_of_hours': tareo_detail.vdi_co*8,
                        'amount': 0,
                    }
                    res.append(VDI)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_vre')
                    VRE = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.vre_co,
                        'number_of_hours': tareo_detail.vre_co*8,
                        'amount': 0,
                    }
                    res.append(VRE)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_anr')
                    ANR = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.lnr_co,
                        'number_of_hours': tareo_detail.lnr_co*8,
                        'amount': 0,
                    }
                    res.append(ANR)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_sln')
                    SLN = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.sln_co,
                        'number_of_hours': tareo_detail.sln_co*8,
                        'amount': 0,
                    }
                    res.append(SLN)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_lr')
                    LR = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.lr_co,
                        'number_of_hours': tareo_detail.lr_co*8,
                        'amount': 0,
                    }
                    res.append(LR)

                    work_entry_type=self.env.ref('hr_tareo.work_entry_type_lt')
                    LT = {
                        'sequence': work_entry_type.sequence,
                        'work_entry_type_id': work_entry_type.id,
                        'number_of_days': tareo_detail.lt_co,
                        'number_of_hours': tareo_detail.lt_co*8,
                        'amount': 0,
                    }
                    res.append(LT)

        return res

    def write(self, vals):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        if 'period_id' in vals:
            if not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede modificar este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(HrPayslip, self).write(vals)

    def unlink(self):
        if not self.period_id.check_state_period():
            raise ValidationError('No se puede modificar este registro ya que el periodo '+self.period_id.name+' se encuentra cerrado')
        return super(HrPayslip, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'period_id' in vals and not self.env['hr.payroll.period'].browse(vals['period_id']).check_state_period():
                raise ValidationError('No se puede crear este registro ya que el periodo '+self.env['hr.payroll.period'].browse(vals['period_id']).name+' se encuentra cerrado')
        return super(HrPayslip, self).create(vals_list)

class HRWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    country_id = fields.Many2one('res.country','País')