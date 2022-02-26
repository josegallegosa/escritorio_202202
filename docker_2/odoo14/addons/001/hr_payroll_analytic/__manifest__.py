# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Payroll Analytic',
    'version': '1.1',
    'category': 'Generic Modules/Human Resources',
    'description': """
        Payroll Analytic

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https:www.rapi.tech',
    'depends': [
        'hr_payroll','hr_contract','account'
    ],
    'init_xml': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_eps_analytic.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
