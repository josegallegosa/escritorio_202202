# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Others incomes and expenses',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Others incomes and expenses
==============================
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll'
    ],
    'init_xml': [
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/hr_others_incomes_expenses.xml',
        'wizards/wizard.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
