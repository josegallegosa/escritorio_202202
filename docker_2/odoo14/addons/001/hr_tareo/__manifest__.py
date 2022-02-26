# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Novedades',
    'version': '1.7',
    'category': 'Generic Modules/Human Resources',
    'description': """
Department Novedades
=====================================================

Easily create, manage, and track employee schedules.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_payroll','hr_payroll_period'
    ],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/hr_tareo_view.xml',
    ],
    'installable': True,
    'active': False,
}
