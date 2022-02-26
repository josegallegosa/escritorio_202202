# -*- coding: utf-8 -*-
##############################################################################

from odoo import fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

YEAR_SELECTION = [(str(year), year) for year in range(2018, int(datetime.now().strftime('%Y'))+5)]

class TxtWizardExport(models.TransientModel):
    _name = 'txt.wizard.generate.period'
    _description = 'Generar Periodos'

    year = fields.Selection(string="Año",selection=YEAR_SELECTION, default=datetime.now().strftime('%Y'))

    frequency = fields.Selection(
        string="Frecuencia",
        selection=[
            ('monthly', 'Mensual'),
            ('biweekly', 'Quincenal'),
        ], default="monthly"
    )   

    def validate_period_repeat(self, lista, i):
        for periodo in lista:
            if date(int(self.year),i+1,1) == periodo.date_start:
                raise ValidationError('Intenta crear un periodo existente!!!')
                return True
                break

    def generate_periodo(self):

        meses = ['ENERO','FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SEPTIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE']
        quinc = 0

        list_periodo_exist = self.env['hr.payroll.period'].search([('state', '=', 'open')])
  

        if self.frequency == 'monthly':
            for i in range(0,12):
                if i == 11:
                    date_end = date(int(self.year)+1,1,1) +relativedelta(days=-1)
                else:
                    date_end = date(int(self.year),i+2,1)+relativedelta(days=-1)
                vals={'name':str(meses[i])+' '+self.year+' MENSUAL',
                    'date_start':date(int(self.year),i+1,1),
                    'date_end':date_end,}
                if self.validate_period_repeat(list_periodo_exist,i):
                    break
                else:
                    line = self.env['hr.payroll.period'].create(vals)
        elif self.frequency == 'biweekly':
            for i in range(0,24):
                quinc = i//2
                if i%2 == 1:
                    if quinc == 11:
                        date_end = date(int(self.year)+1,1,1) +relativedelta(days=-1)
                    else:
                        date_end = date(int(self.year),quinc+2,1)+relativedelta(days=-1)
                    vals={'name':str(meses[quinc])+' '+self.year+' 2Q',
                        'date_start':date(int(self.year),quinc+1,15),
                        'date_end':date_end,}
                    if self.validate_period_repeat(list_periodo_exist,i):
                        break
                    else:
                        line = self.env['hr.payroll.period'].create(vals)
                else:
                    if quinc == 11:
                        date_end = date(int(self.year)+1,1,15) +relativedelta(months=-1)
                    else:
                        date_end = date(int(self.year),quinc+2,15)+relativedelta(months=-1)
                    vals={'name':str(meses[quinc])+' '+self.year+' 1Q',
                        'date_start':date(int(self.year),quinc+1,1),
                        'date_end':date_end,}
                    if self.validate_period_repeat(list_periodo_exist,i):
                        break
                    else:
                        line = self.env['hr.payroll.period'].create(vals)

       
class hr_payroll_period(models.Model):

    _name = 'hr.payroll.period'
    _description = 'Payroll Period'

    _inherit = ['mail.thread']

    name = fields.Char(string='Descripción', size=256, required=True)
    date_start = fields.Date(string='Fecha de inicio', required=True)
    date_end = fields.Date(string='Fecha de fin', required=True)
    state = fields.Selection([('open','Abierto'),('closed','Cerrado')],
        default='open', readonly=False)
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.user.company_id,
        required=True, index=True, readonly=True)
    _order = "date_start, name desc"

    def open_period(self):
        for period in self:
            period.write({'state':'open'})

    def close_period(self):
        for period in self:
            period.write({'state':'closed'})

    def check_state_period(self):
        if self.state == 'closed':
            return False
        else:
            return True

    def generate_wizard_period(self):
        action = self.env.ref('hr_payroll_period.txt_wizard_generate_period_wizard_action').read()[0]

        action['views'] = [(self.env.ref('hr_payroll_period.txt_wizard_generate_period_form_view1').id, 'form')]

        return action

        

    
        

