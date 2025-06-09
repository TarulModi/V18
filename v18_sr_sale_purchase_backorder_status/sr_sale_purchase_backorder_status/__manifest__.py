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
    'name': "Back Order Status in Sales And Purchase Order",
    'version': "18.0.0.0",
    'summary': "Back Order Status in Sales And Purchase Order",
    'category': 'Extra Addons',
    'description': """
    Back Order Status in Sales And Purchase Order
    Back order status in sales order
    Back order status in purchase order
    Back order status
    sales back order status
    purchase back order status
    Sales Back order
    Purchase Back order
    how to track back orders from sales
    how to track back orders from purchase
    """,
    'author': "Sitaram",
    'website':"www.sitaramsolutions.in",
    'depends': ['base','sale','purchase', 'stock', 'sale_management'],
    'data': [
        'views/sr_inherited_purchase_order.xml',
        'views/sr_inherited_sale_order.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    "price": 10,
    "currency": 'EUR',
    'live_test_url':'https://youtu.be/xXB9Dg8ikQQ',
    'images': ['static/description/banner.png'],
}
