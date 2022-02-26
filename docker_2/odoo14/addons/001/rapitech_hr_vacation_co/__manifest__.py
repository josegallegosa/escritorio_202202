# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Rapitech HR Employee Vacation Colombia',
    'version': '1.0',
    'category': 'Generic Modules/Human Resources',
    'description': """
HR Employee Vacation Colombia
===================================

Gestión de vacaciones Colombia.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll','hr_holidays','rapitech_hr','hr_social_benefits', 'hr_contract'
    ],
    'data': [
        'data/cron_vacation.xml',
        'views/hr_vacation.xml',
        'views/hr_leave.xml',
    ],
    'installable': True,
    'active': False,
}
