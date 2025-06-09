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
    'name': "Import Inventory Adjustment",
    'version': "18.0.0.0",
    'summary': "This module helps you to import bulk products in inventory adjustment",
    'category': 'stock',
    'description': """
        Using this module Inventory adjustment is imported using excel sheets
        import inventory adjustment
        product import in inventory adjustment
        bulk inventory import
        inventory
        import bulk
        import bulk products
        stock increase
        bulk stock
        bulk fill the stock
        bulk increase stock
        products in stock
    """,
    'author': "Sitaram",
    'website': "http://www.sitaramsolutions.in",
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_inventory_adjustment.xml',
    ],
    'live_test_url':'https://youtu.be/E8YMlI2doDg',
    'images': ['static/description/banner.png'],
    "price": 10,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
