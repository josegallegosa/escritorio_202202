# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Rapitech HR Employee Gratification',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Employee Gratification
==============================

Cálculo de Gratificación Perú.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll','hr_payroll_period'
    ],
    'data': [
        'data/hr_data_gratification.xml',
    ],
    'installable': True,
    'active': False,
}
