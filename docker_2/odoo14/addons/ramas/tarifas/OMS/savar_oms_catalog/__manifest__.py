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
                    'web',
                    'website', 
                    'product',
                    'website_form',
                    'website_sale',                  
                    'web_editor',
                    
                    'fieldservice',
                ],
    'data': [                
                'data/groups.xml',
                'views/assets.xml',
                'views/res_partner.xml',
                'views/website/signup.xml',
                'views/website/my_account.xml',
                'views/web_editor.xml',
                'views/website_sale/product_template.xml',
                'views/website_sale/taxes.xml',
                'security/ir.rule.csv',
                'security/ir.model.access.csv',
            ],
    'qweb': [
                #'static/src/xml/website/signup.xml',
            ]

}

#master pass: vpfh-eb2r-3umk