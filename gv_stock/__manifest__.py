# -*- coding: utf-8 -*-
{
    'name': "GVDirect Stock",
    'summary': "stock module changes",
    'description': """
        Description for Internal Transfers field modifications.
    """,
    'author': "Lean Systems",
    'website': "http://www.leansystems.ge",
    'category': 'GVDirect',
    'version': '1.0',
    'depends': ['stock', 'sale_stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'report/report_stockpicking_operations.xml',
        'report/report_deliveryslip.xml',
    ],
    'installable': True,
    'auto_install': False,
}
