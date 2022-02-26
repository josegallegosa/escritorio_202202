# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR 5ta',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR 5TA
======
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': [
        'hr_payroll', 'hr_payroll_parameters'
    ],
    'init_xml': [
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/hr_5ta.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
