# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

{
    'name': "Convert Quotation/Sales Order to Task",
    'version': "18.0.0.0",
    'summary': "Convert Quotation/Sales order to the project task.",
    'category': 'Sales',
    'description': """
        Convert Quotation/Sales order to the project task.
    """,
    'author': "Sitaram",
    'website': " ",
    'depends': ['base', 'sale_management', 'product','project'],
    'data': [
        'views/sale.xml',
        'security/ir.model.access.csv',
        'views/project_task.xml'
    ],
    'demo': [],
    'price': 20.00,
    'currency': 'EUR',
    "license": "OPL-1",
    'images': ['static/description/banner.png'],
    'live_test_url':'https://www.youtube.com/watch?v=MOVBk9uBX5w&t=42s',
    'installable': True,
    'application': True,
    'auto_install': False,
}
