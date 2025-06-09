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
    'name': 'Image In Sales Order, Purchase Orders And Invoice Report',
    'version': '18.0.0.0',
    'category': 'sales',
    "license": "OPL-1",
    'summary': 'This module used to show image in sales order , purchase order and invoice report for product.',
    'description': """
        In this module you can show image in sales order , purchase order and invoice report for product.
""",
    'author': 'Sitaram',
    'depends': ['base','sale','purchase','account'],
    'data': [
             'views/inherit_sale_report.xml',
             'views/inherit_invoice_report.xml',
            'views/inherit_purchase_report.xml',
            'views/inherit_purchase_rfq_report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/pGsyVW5euh4',
    "images":['static/description/banner.png'],
    'website': "www.sitaramsolutions.in",
}
