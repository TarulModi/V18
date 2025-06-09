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
    'name': "Invoice Smart Button In Product",
    'version': "18.0.0.0",
    'summary': "This module provides 2 smart buttons to show product QTY and Amount for a particular product.",
    'website': ' ',
    "license": "OPL-1",
    'category': 'Products',
    'description': """This module provides 2 smart buttons to show product QTY and Amount for a particular product.""",
    'author': 'Sitaram',
    'depends': ['base', 'account', 'product'],

    'data': [
        'views/product_view.xml',
    ],
    'demo': [],
    "price": 10,
    "currency": 'EUR',
    'live_test_url': 'https://youtu.be/cDwoE_TRXKI',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
