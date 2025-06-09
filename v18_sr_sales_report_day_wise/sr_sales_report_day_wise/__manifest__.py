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
    'name': "Day Wise Sales Report",
    'version': "18.0.0.0",
    'summary': "This module is useful to generate sales report of products days wise.",
    'category': 'Extra Tools',
    "license": "OPL-1",
    "price": 15,
    "currency": 'EUR',
    'description': """
    This module is useful to generate sales report of products days wise.
    """,
    'author': "Sitaram",
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/daily_sales_report_wizard.xml',
        'report/report_daywise_template.xml',
        'report/report.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'live_test_url': 'https://youtu.be/1WEYqmZUQCs',
    'installable': True,
    'application': False,
    'auto_install': False,
}