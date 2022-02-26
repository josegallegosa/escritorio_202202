# -*- coding: utf-8 -*-
##############################################################################

{
    'name': 'Importar Novedades',
    'version': '1.2',
    'category': 'Generic Modules/Human Resources',
    'description': """
Importar Novedades
===============
Importa de manera fácil las novedades de los empleados.
    """,
    'author': 'Rapid Technologies SAC',
    'website': 'http://www.rapi.tech',
    'depends': [
        'hr_tareo',
    ],
    'init_xml': [
    ],
    'data': [
        'views/hr_tareo_view.xml',
    ],
    'test': [
    ],
    'demo_xml': [
    ],
    'installable': True,
    'active': False,
}