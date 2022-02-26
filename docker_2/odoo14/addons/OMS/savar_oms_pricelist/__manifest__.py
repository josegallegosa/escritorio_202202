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
        'sale',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',

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

        'views/price_list/fsm_order_service_views.xml',
        'views/price_list/ubigeo_views.xml',
        'views/price_list/storage_views.xml',
        'views/price_list/labeling_product_views.xml',
        'views/price_list/labeling_package_views.xml',
        'views/price_list/by_weight_views.xml',
        'views/price_list/product_size_views.xml',
        'views/price_list/by_package_views.xml',
        'views/price_list/payment_type_views.xml',
        'views/price_list/picking_views.xml',
        'views/price_list/packing_views.xml',
        'views/price_list/by_pick_up_views.xml',
        'views/price_list/by_sure_views.xml',
        'views/price_list/back_office_views.xml',
        'views/price_list/prints_views.xml',
      
        'views/sale_order_views.xml',
        'views/oms_pricelist_views.xml',
        'views/menuitem_views.xml',       
    ],
}
