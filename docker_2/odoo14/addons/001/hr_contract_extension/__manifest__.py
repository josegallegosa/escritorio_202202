# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR CONTRACT EXTENSION',
    'version': '1.1',
    'category': 'Human Resources',
    'description': """

HR CONTRACT EXTENSION
======================

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': ['hr_contract','hr_payroll','rapitech_hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

