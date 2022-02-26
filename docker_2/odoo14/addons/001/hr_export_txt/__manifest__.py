# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR EXPORT TXT',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

HR EXPORT TXT
======================


    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapid.tech',
    'depends': ['hr_contract','hr_payroll','hr_payroll_period'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'wizards/wizard.xml',
    ],
    'installable': True,
    'auto_install': False,
}

