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
    'name': 'Add Serial Number Via Barcode On Incoming and Outgoing Pickings/Shipments',
    'version': '18.0.0.0',
    'category': 'Warehouse Management',
    "license": "OPL-1",
    'summary': 'This module will easy to add products lot and serial number via scanner in incoming and outgoing shipments',
    'description': """
    This module will easy to add products lot and serial number via scanner in incoming and outgoing shipments
    easy to scan barcode
    easy to add serial number
    easy to add lot number
    scan serial number for picking
    scan serial number for incoming shipment
    scan serial number for outgoing shipment
    scan lot number for picking
    scan lot number for incoming shipment
    scan lot number for outgoing shipment
    easy to add via barcode scanner
    serial number via barcode scanner for picking
    serial number via barcode scanner for incoming shipment
    serial number via barcode scanner for outgoing shipment
    lot number via barcode scanner for picking
    lot number via barcode scanner for incoming shipment
    lot number via barcode scanner for outgoing shipment
    scan barcode on picking
    barcode scan on picking
    scan barcode on incoming shipment
    barcode scan on outgoing shipment
    scan barcode on Delivery orders
    barcode scan on receipts
    
""",
    "price": 50,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base','sale_management','purchase','stock'],
    'data': [
             'views/sr_inherit_stock_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/uoXGXrLgd8Y',
    "images":['static/description/banner.png'],
    'website': "https://sitaramsolutions.in",
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
