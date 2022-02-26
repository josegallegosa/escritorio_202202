# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Loan Employee',
    'version': '1.1',
    'category': 'Generic Modules/Human Resources',
    'description': """
        HR PRESTAMOS
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': [
        'hr_payroll', 'hr_others_incomes_expenses'
    ],
    'init_xml': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
