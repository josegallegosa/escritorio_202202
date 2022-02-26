# -*- coding: utf-8 -*-

{
    'name': 'MRP Tracking',
    'category': 'MRP',
    'summary': 'Tracking MRP',
    'version': '13.0.2',
    'description': """Tracking MRP""",
    'author': 'Rapid Technologies SAC',
    'website': 'https://www.rapi.tech',
    'depends': ['mrp','qa_location_world'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/wizard.xml',
        'views/view.xml',
    ],
    'installable': True,
    
}
