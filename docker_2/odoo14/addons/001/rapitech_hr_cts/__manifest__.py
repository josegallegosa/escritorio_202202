# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Rapitech HR Employee CTS',
    'version': '1.1',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Employee CTS
=================

Cálculo de CTS.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll','hr_payroll_period','hr_payroll_rg','rapitech_hr_gratification'
    ],
    'data': [
        'data/hr_data_cts.xml',
    ],
    'installable': True,
    'active': False,
}
