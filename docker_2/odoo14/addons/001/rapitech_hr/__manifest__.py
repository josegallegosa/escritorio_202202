# -*- coding: utf-8 -*-
{
    'name': "Rapitech HR Employee",

    'summary': """
    	Modificaciones HR Employee
    """,

    'description': """
        Actualizaciones HR
    """,

    'author': "Rapid Technologies SAC",
    'website': "www.rapi.tech",

    'category': 'Employee',
    'version': '0.8',

    'depends': ['base','account','hr','l10n_latam_base','hr_payroll_period','l10n_co','hr_contract','hr_payroll_account'],

    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_maestros_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',
        'views/report_view.xml',
        'views/res_bank_view.xml',
        'views/res_partner_bank_view.xml',
        'views/res_partner_view.xml',
        'views/hr_salary_rule_view.xml',
        'data/ir_sequence_data.xml',
        'data/hr.type.employee.csv',
        'data/l10n_latam.identification.type.csv',
        'data/masters.xml',
        'data/res_bank_data.xml',
        'data/hr_pension_fund_data.xml',
        'data/hr_arl_data.xml',
        'data/hr_eps_data.xml',
        'data/hr_ccf_data.xml',
        'data/hr_type_contributor_data.xml',
        'data/hr_subtype_contributor_data.xml',
        'data/hr_type_layoffs_data.xml',
        'data/hr_type_transport_data.xml',
        'data/hr_withholding_procedure_data.xml',
        'data/hr_type_risk_arl_data.xml',
        'data/account_type.xml',
        'data/hr_country_department.xml',
        'data/hr_country_city.xml',
        'data/hr_type_contract.xml',

    ],
}
