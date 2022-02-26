# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Rapitech HR Payroll Account Colombia',
    'version': '14.0.2',
    'category': 'Generic Modules/Human Resources',
    'description': """
        Payroll Account Colombia
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll_account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_contract_view_inherit.xml',
        'views/account_journal_inherit.xml'
    ],
    'installable': True,
}
