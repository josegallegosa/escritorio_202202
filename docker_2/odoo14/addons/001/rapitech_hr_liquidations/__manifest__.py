# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Rapitech HR Employee Liquidations',
    'version': '1.6',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Employee Liquidations
==============================

Cálculo de Liquidaciones Colombia.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll','hr_payroll_period','rapitech_hr_gratification','rapitech_hr_cts','structure_layoffs'
    ],
    'data': [
        'data/hr_data_liquidations.xml',
    ],
    'installable': True,
    'active': False,
}
