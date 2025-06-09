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
    'name': "POS Product Expiry Alert And Email Notification",
    'version': "18.0.0.0",
    'summary': "This module helps you to get Alert on POS and Send daily email notification to the inventory manager for product expiry",
    'category': 'Warehouse',
    'description': """
    stock Alert
    product expiry Alert
    lot product expiry Alert
    out of date Alert
    pos lot expiry Alert
    pos Alert
    expired product Alert
    lot expiry notification email
    email to the inventory manager
    email notification
    email
    notification
    out of date product notification
    out of date product email notification
    inventory manager will be notified for out of date product
    product end cycle email notification
    product end cycle warning in pos
    
    
    """,
    'author': "Sitaram",
    'website': "sitaramsolutions.in",
    'depends': ['base','point_of_sale', 'product_expiry'],
    'data': [
        'data/email_template.xml',
        'data/expiry_cron.xml',
        # 'views/sr_pos_product_expiry_notification.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'sr_pos_product_expiry_notification/static/src/js/pos.js'
        ],
    },
    'live_test_url':'https://youtu.be/RfIQWbUDV2I',
    'images': ['static/description/banner.png'],
    "price": 10,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}