# -*- coding: utf-8 -*-
{
    'name': "Módulo de Configuración Italtel",

    'summary': """
    muestra un subtitulo del módulo
      
    """,

    'description': """
    Siempre documentar el resumen o descripcion
    """,

    'author': "Jose Gallegos",
    'website': "https://re-odoo-10.readthedocs.io/capitulos/construyendo-tu-primera-aplicacion-odoo/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/income_type_views.xml',
        'views/income_views.xml',
        'views/menuitem_views.xml',
        'data/income_type.xml',
        'data/income.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
}
