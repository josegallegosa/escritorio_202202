{
    'name': """
	    Savar TMS Field Service
    """,

    'summary': """
    """,

    'description': """
    """,

    'category': 'Warehouse',
    'version': '14.0',

    'depends': [        
        'fieldservice','odoope_toponyms','base',        
    ],

    'data': [
        'views/fsm_location.xml',
        'views/res_partner.xml',
        'data/res_partner.xml',
        'data/ubigeo.xml'
    ],

    'images': ['static/description/banner.png'],

    'application': True,
    'installable': True,
    'auto_install': False,
    "sequence": 1,
}
