# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Payroll Period',
    'version': '1.1',
    'category': 'Localization',
    'description': """
Payroll Period 
===============
This module implements a period for payroll.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http:www.rapi.tech',
    'depends': [
        'hr_payroll','hr_work_entry_contract'
    ],
    'qweb': [
        'static/src/xml/button_header.xml',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_payroll_period_view.xml',
        'views/button_generate_period.xml',
        'wizards/wizard.xml',
    ],
    
    'installable': True,
    'active': False,
}
