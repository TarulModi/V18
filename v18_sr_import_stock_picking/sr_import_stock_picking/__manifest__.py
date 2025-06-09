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
    'name': "Import Stock Picking",
    'version': "18.0.0.1",
    'summary': "This module helps you to import Stock Picking",
    'category': 'Inventory/Inventory',
    'description': """
        Using this module Stock Picking is imported using excel sheets
    import stock picking
    """,
    'author': "Sitaram",
    'website':"https://sitaramsolutions.in",
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_stock_picking_view.xml',
        
    ],
    'live_test_url':'https://youtu.be/q8-um-wX7tI',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
