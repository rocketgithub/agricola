# -*- coding: utf-8 -*-
{
    'name': "Agricola",

    'summary': """ Módulo para RRHH de empresas agropecuarias """,

    'description': """
         Módulo para RRHH de empresas agropecuarias
    """,

    'author': "Rodolfo Borstcheff",
    'website': "http://www.aquih.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'hr_timesheet','hr_payroll'],

    'data': [
        'views/agricola_views.xml',
        'views/account_views.xml',
        'views/proyect_views.xml',
        'views/hr_payroll_views.xml',
    ],
}
