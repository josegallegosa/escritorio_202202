# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'HR Plame',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """

Peruvian Plame
======================
ADD tables SUNAT plame.

    """,
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapid.tech',
    'depends': ['hr_payroll'],
    'data': [
        'data/hr_table_22_category_data.xml',
        'data/hr_table_22_data.xml',
        'security/ir.model.access.csv',
        'views/hr_plame.xml',
    ],
    'installable': True,
    'auto_install': False,
}

