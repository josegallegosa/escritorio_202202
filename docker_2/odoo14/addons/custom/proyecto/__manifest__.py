# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Subscription',
    'version': '1.6',
    'category': 'Sales/Sales',
    'depends': ['product','stock','purchase','sale','purchase'],
    'description': """
Extension para productos de librería
=====================================
Añade varios campos necesarios para la gestión de una librería.
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/sale_subscrition.xml',
        
    ],
    'installable': True,
    'auto_install': False,
}
