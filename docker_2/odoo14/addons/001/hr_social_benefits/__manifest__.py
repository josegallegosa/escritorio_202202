# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Beneficios Sociales',
    'version': '14.0.3',
    'category': 'Human Resources',
    'description': """
        HR Generation Plame.
        This application generate pdt files
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': ['hr_contract','account', 'hr_payroll', 'hr_holidays','hr_payroll_rg_co'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/hr_novelty.xml',
        'views/hr_contract.xml',
        'data/hr_leave_type.xml',
    ],
    'installable': True,
    'auto_install': False,
}
