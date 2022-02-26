# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Recalculation pr2',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Recalculation pr2
======
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https:www.rapi.tech',
    'depends': [
        'hr_payroll','hr','hr_payroll_period','hr_contract'
    ],
    'init_xml': [
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_recalculation_pr2.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}
