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
    'name': "Sales Stock Reservation",
    'version': "18.0.0.0",
    'summary': "This module helps you to reserve your stock in odoo",
    'category': 'Sale',
    'description': """
    This module is used to reserve your stock in odoo
    booking
    advance booking
    reservation
    stock reservation
    layaway stratagy 
    online book your stock
    remainder of reserve stock
    product advance booking
    product booking
    book your product 
    block your product
    hold your favorite stock
    
    """,
    'author': "Sitaram",
    'website': "sitaramsolutions.in",
    'depends': ['base','sale_management','stock'],
    'data': [
        'data/ir_cron_data.xml',
        'views/inherit_sale_orders_view.xml',
        'views/inherited_product.xml',
        'views/inherit_res_config_view.xml'
    ],
    'live_test_url':'https://youtu.be/l6XXXicgfoo',
    'images': ['static/description/banner.png'],
    "price": 15,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
