# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Payroll RIA',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

Peruvian Payroll Rules RIA
This application add rules and structures salary.

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': ['base','hr_contract','rapitech_hr','hr_payroll_period', 'hr_plame', 'hr_5ta','hr_eps','hr_tareo','hr_others_incomes_expenses','hr_payroll_parameters'],
    'data': [
        'data/hr_payroll_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
