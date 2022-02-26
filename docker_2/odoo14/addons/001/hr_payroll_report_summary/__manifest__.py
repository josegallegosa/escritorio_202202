# -*- coding: utf-8 -*-
{
    'name': "Resumen de Planilla",
    'summary': """
    	Modificaciones HR Payroll 
    """,
    'description': """
        Reporte de Nómina HR
    """,
    'author': "Rapid Technologies SAC",
    'website': "www.rapi.tech",
    'category': 'Payroll',
    'version': '13.0.1',
    'depends': ['base','hr_payroll','rapitech_hr',
        'hr_tareo'],
    'data': [
        #'security/ir.model.access.csv',

        'data/data.xml',
        'views/view.xml',
        'views/report.xml',


    ],
}
