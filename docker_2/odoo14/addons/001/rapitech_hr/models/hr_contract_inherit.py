from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class HRTypeContract(models.Model):
    _name = 'hr.type.contract'
    _description = 'Tipo de contrato'

    name = fields.Char(string='Tipo de contrato')
    code = fields.Char(string='Código')
    country_id = fields.Many2one('res.country', string='País')

class res_partner(models.Model):
    _inherit = 'hr.contract'

    code = fields.Char(string="Código", readonly=True)
    
    type_contract = fields.Many2one(comodel_name='hr.type.contract',string='Tipo de Contrato', ondelete='restrict')	

    reason_termination = fields.Selection(
    	string="Motivo de Cese",
    	selection=[
    		('resignation', 'Renuncia'),
    		('unjust_cause', 'Terminación Unilateral'),
    	]
    )

    @api.model
    def create(self, vals):
        vals['code'] = self.env['ir.sequence'].next_by_code('contract.order') or _('New')
        
        employee = self.env['hr.employee'].search([('id','=',int(vals['employee_id']))])
        
        if vals['employee_id']:
            vals['name'] = vals['code'] + ' ' + employee.name
        else:
            vals['name'] = vals['code']

        type_contract_id_fixed_term = self.env.ref('rapitech_hr.hr_type_contract_1').id
        type_contract_id_indefinite_term = self.env.ref('rapitech_hr.hr_type_contract_2').id

        if vals['type_contract'] == type_contract_id_fixed_term and vals['date_end'] == False:
            raise ValidationError('El Contrato con tipo de Contrato a "Termino Fijo" debe tener obligatoriamente una fecha final')

        if vals['type_contract'] == type_contract_id_indefinite_term and vals['date_end'] != False and vals['reason_termination'] ==False:
            raise ValidationError('El Contrato con tipo de Contrato a "Termino Indefinido" cuando tiene una fecha final debe tener obligatoriamente un motivo de cese')


        result = super(res_partner, self).create(vals)
        return result
    """
    @api.depends('date_end')
    def _onchange_date_end(self):
        print("cambio en date_end")
        self.type_contract = ''
        

    def write(self, vals):
        

        type_contract_id_fixed_term = self.env.ref('rapitech_hr.hr_type_contract_1').id
        type_contract_id_indefinite_term = self.env.ref('rapitech_hr.hr_type_contract_2').id

        if vals['type_contract'] == type_contract_id_fixed_term and vals.get('date_end', False) == False:
            raise ValidationError('El Contrato con tipo de Contrato a "Termino Fijo" debe tener obligatoriamente una fecha final')


        if vals['type_contract'] == type_contract_id_indefinite_term and vals.get('date_end', False) != False and vals.get('reason_termination', False) ==False:
            raise ValidationError('El Contrato con tipo de Contrato a "Termino Indefinido" cuando tiene una fecha final debe tener obligatoriamente un motivo de cese')


        result = super(res_partner, self).write(vals)
        return result
    """
    @api.onchange('employee_id')
    def _onchange_name(self):
        
        if self.employee_id:
            employee = self.env['hr.employee'].search([('id','=',self.employee_id.id)])

            self.name = employee.name

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            struct_id = self.env.ref('hr_payroll_rg_co.structure_s_t_co').id
            structure_type = self.env['hr.payroll.structure.type'].search([
                ('default_struct_id', '=', struct_id)])
            if structure_type:
                self.structure_type_id = structure_type
            else:
                self.structure_type_id = False

    
