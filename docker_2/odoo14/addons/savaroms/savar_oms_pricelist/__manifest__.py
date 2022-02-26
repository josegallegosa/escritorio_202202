# -*- coding: utf-8 -*-
{
    'name': "Tarifas Savar",

    'summary': """
     """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.instagram.com/rockscripts",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'base',
        'fieldservice',
        'savar_tms_fms',
    ],
    'data': [
        'data/service.xml',
        'data/subservice.xml',
        'data/ubigeo.xml',
        'data/storage.xml',
        'data/labeling_product.xml',
        'data/labeling_package.xml',
        'data/by_weight.xml',
        'data/product_size.xml',
        'data/by_package.xml',
        'data/payment_type.xml',
        'data/picking.xml',
        'data/packing.xml',
        'data/by_pick_up.xml',
        'data/by_sure.xml',
        'data/back_office.xml',
        'data/prints.xml',
        'data/type_order.xml',
        'views/product_size_views.xml',
        'views/oms_pricelist_views.xml',
        'views/sale_order_views.xml',
        'views/menuitem_views.xml',
        #'security/ir.model.access.csv',
    ],
}
