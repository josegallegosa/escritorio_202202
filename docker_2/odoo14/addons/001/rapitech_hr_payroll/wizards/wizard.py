# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    VALUES = [('1','Salario'),('2','Liquidación'),('3','Cesantias')]
    salary_type = fields.Selection(selection = VALUES,
        string='Tipo de nómina', default="1")

    @api.onchange('salary_type')
    def onchange_structure_employees(self):
        payslip_run_id = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))
        
        contracts_ids = self.env['hr.contract'].search([('date_end', '<', payslip_run_id.date_end),('date_end', '>=', payslip_run_id.date_start)]).ids

        #valido los payslips existentes
        list_payslips_existing = []
        for payslip in payslip_run_id.slip_ids:
            list_payslips_existing.append(payslip.employee_id.id)

        

        self.employee_ids = False
        if self.salary_type in ('1','3'):
            employee_ids = self.env['hr.employee'].search([
                ('contract_ids.state', 'in', ('open', 'close')),
                ('company_id', '=', self.env.company.id),
                ('contract_id','not in', contracts_ids),
                ('id','not in', list_payslips_existing)]) #si la nomina existe no se filtra automáticamente
        else:
            employee_ids = self.env['hr.employee'].search([
                ('contract_ids.state', 'in', ('open', 'close')),
                ('company_id', '=', self.env.company.id),
                ('contract_id','in', contracts_ids),
                ('id','not in', list_payslips_existing)]) #si la nomina existe no se filtra automáticamente
        self.employee_ids = employee_ids.ids

        

    def compute_sheet(self):

        self.ensure_one()
        if not self.env.context.get('active_id'):
            from_date = fields.Date.to_date(self.env.context.get('default_date_start'))
            end_date = fields.Date.to_date(self.env.context.get('default_date_end'))
            payslip_run = self.env['hr.payslip.run'].create({
                'name': from_date.strftime('%B %Y'),
                'date_start': from_date,
                'date_end': end_date,
            })
        else:
            payslip_run = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        employees = self.with_context(active_test=False).employee_ids
        if not employees:
            raise UserError("You must select employee(s) to generate payslip(s).")

        payslips = self.env['hr.payslip']
        Payslip = self.env['hr.payslip']

        contracts = employees._get_contracts(
            payslip_run.date_start, payslip_run.date_end, states=['open', 'close']
        ).filtered(lambda c: c.active)
        contracts._generate_work_entries(payslip_run.date_start, payslip_run.date_end)
        work_entries = self.env['hr.work.entry'].search([
            ('date_start', '<=', payslip_run.date_end),
            ('date_stop', '>=', payslip_run.date_start),
            ('employee_id', 'in', employees.ids),
        ])
        self._check_undefined_slots(work_entries, payslip_run)


        if self.salary_type == '2':
            struct_id = struct_id_cesa = self.env.ref('rapitech_hr_liquidations.structure_liq_co').id
        if self.salary_type == '3':
            struct_id = struct_id_cesa = self.env.ref('structure_layoffs.structure_cesa_co').id

        default_values = Payslip.default_get(Payslip.fields_get())

        payslip_run_id = self.env['hr.payslip.run'].browse(self.env.context.get('active_id'))

        salary_type_name = ''
        salary_type_name_id = ''
        for x in self.VALUES:
            if self.salary_type == x[0]:
                salary_type_name = x[1]
                salary_type_name_id = x[0] 
        payslip_run_id.salary_type = salary_type_name

        list_payslips_existing = []
        list_payslip_run_id = self.env['hr.payslip.run'].search([])
        for payslip in payslip_run_id.slip_ids:
            list_payslips_existing.append(payslip.contract_id.id)
        print("list_payslips_existing ",list_payslips_existing)
        boolean = False
        
        for x in list_payslip_run_id:
            if x.period_id == payslip_run_id.period_id and x.salary_type == payslip_run_id.salary_type and x.id != payslip_run_id.id:
                raise ValidationError('Intenta generar nominas a un lote con el mismo "tipo de nomina", asociada a un mismo periodo de otro lote')
        
        if self.salary_type != salary_type_name_id:
                raise ValidationError('Intenta generar nominas con diferente "tipo de nomina" al lote actual')

        for contract in contracts:
            if self.salary_type == '1':
                struct_id = contract.structure_type_id.default_struct_id.id
            for contract_id in list_payslips_existing:
                if contract_id == contract.id:
                    raise ValidationError('Intenta crear un payslip a un empleado que ya se generó previamente')
                    boolean = True
                    break

            if boolean:
                break
            values = dict(default_values, **{
                'employee_id': contract.employee_id.id,
                'credit_note': payslip_run.credit_note,
                'payslip_run_id': payslip_run.id,
                'date_from': payslip_run.date_start,
                'date_to': payslip_run.date_end,
                'contract_id': contract.id,
                'struct_id': struct_id,
                'period_id': payslip_run.period_id.id
            })
            payslip = self.env['hr.payslip'].new(values)
            payslip._onchange_employee()
            values = payslip._convert_to_write(payslip._cache)
            payslips += Payslip.create(values)
        payslips.compute_sheet()
        payslip_run.state = 'verify'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip.run',
            'views': [[False, 'form']],
            'res_id': payslip_run.id,
        }