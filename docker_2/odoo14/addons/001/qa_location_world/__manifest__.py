# -*- coding: utf-8 -*-
{
    'name': "QA Location World",

    'summary': """
        QA Location World""",

    'description': """
        QA Location World
    """,

    'author': "GRUPO QUANAM S.A.C.",
    'website': "https://www.grupoquanam.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Personalization',
    'version': '0.1',
    'sequence': 0,

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'mrp',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        # 'views/templates.xml',
    ]
}
