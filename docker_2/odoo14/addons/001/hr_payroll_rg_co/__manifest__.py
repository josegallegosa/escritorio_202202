# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Payroll General Regimen CO',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

Colombian Payroll Rules RG
=================================================
This application add rules and structures salary.

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': ['base','hr_contract','rapitech_hr','hr_payroll_period', 'hr_plame', 'hr_5ta','hr_eps','hr_tareo','hr_others_incomes_expenses','hr_payroll_parameters','hr_export_payroll','hr_import_tareo','hr_loan'],
    'data': [
        'data/hr_payroll_data_s_t.xml',
        'data/hr_payroll_data_s_i.xml',
        'data/hr_payroll_data_a_s_e_l.xml',
        'data/hr_payroll_data_a_s_e_p.xml',
        
    ],
    'installable': True,
    'auto_install': False,
}


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
