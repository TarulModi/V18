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
    'name': 'Mass Confirm Delivery Orders from Sales',
    'version': '18.0.0.0',
    'category': 'Warehouse Management',
    "license": "OPL-1",
    'summary': 'This module will help you to validate multiple delivery orders from multiple sales order.',
    'description': """
        This module use to select sales order and validate outgoing delivery orders from tree view.
        mass validate outgoing shipment
        mass validate stock picking
        mass validate sales picking
        automate sales process
        auto validate multiple picking from sales order
        process multiple outgoing shipment from sales orders
        auto validate shipment
        validate multiple shipment
        warehouse management
        shipment automate
        mass finish delivery order from sale order
        mass confirm delivery order from sale order
        mass done delivery order from sale order
        multiple outgoing shipment validate automatic
        mass finish picking from sale order
        mass confirm picking from sale order
        mass done picking from sale order
        multiple sales shipment validate automatic
        mass finish outgoing shipment from sale order
        mass confirm outgoing shipment from sale order
        mass done outgoing shipment from sale order
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base','sale_management','stock'],
    'data': [
            'security/ir.model.access.csv',
             'views/sr_mass_confirm_delivery_orders.xml',
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/MDW_eB41QHk',
    "images":['static/description/banner.png'],
}
