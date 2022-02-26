# -*- coding: utf-8 -*-
{
    'name': "Modulo de Proyectos by Andres de la Puente",

    'summary': """
    Módulo para gestión de proyectos 
      
    """,

    'description': """
    
    """,

    'author': "Andres de la Puente",
    'website': "https://re-odoo-10.readthedocs.io/capitulos/construyendo-tu-primera-aplicacion-odoo/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','hr','contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        
        'data/departament.xml',
        'data/employee.xml',
        'data/res_user.xml',
        'data/groups.xml',
        
        #'views/departament.xml',
        'views/view_task_form_inherit.xml',
        'views/project_project_form_inherit.xml',
        'views/hr_employee_form_inherit.xml',
        #'views/menuitem_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'application': True,
    "sequence": 1,
}
