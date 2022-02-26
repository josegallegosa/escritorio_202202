# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Parameters',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Parameters
=============
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll',
    ],
    'init_xml': [
    ],
    'data': [
        'data/data.xml',
        'views/payroll_parameters.xml',
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
