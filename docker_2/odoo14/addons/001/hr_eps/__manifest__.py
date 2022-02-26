# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR EPS',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR EPS
======
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https:www.rapi.tech',
    'depends': [
        'hr_payroll'
    ],
    'init_xml': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_eps.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
