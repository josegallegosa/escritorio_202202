# -*- coding: utf-8 -*-
{
    'name': "savar_oms_catalog",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.instagram.com/rockscripts",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
                    'base', 
                    'account', 
                    'sale',
                    'web',
                    'website', 
                    'product',
                    'website_form',
                    'website_sale',
                    'web_editor',
                    'portal',
                    'website_webkul_addons',
                    'website_mega_menus',
                    'savar_tms_fms'
                ],
    'data': [                
                #'data/groups.xml',
                'data/sequence.xml',
                'views/models/res_partner.xml',
                'views/models/product_template.xml',
                'views/models/sale_order.xml',
                'views/assets/frontend.xml',
                'views/web/web_editor.xml',                
                'views/website/signup.xml',
                'views/website/my_account.xml',
                'views/website_sale/product_template_extra_fields.xml',
                'views/website_sale/taxes.xml',
                'views/website_sale/product_template_categories.xml',
                'views/account/merchant_categories.xml',
                'views/account/pages/categories.xml',
                'views/account/merchant_orders.xml',
                'views/account/pages/orders.xml',
                'views/account/merchant_new_order.xml',
                'views/account/pages/new_order.xml',
                'views/account/pages/edit_order.xml',
                #'security/ir.rule.csv',
                #'security/ir.model.access.csv',
            ],
    'qweb': [
            ]

}