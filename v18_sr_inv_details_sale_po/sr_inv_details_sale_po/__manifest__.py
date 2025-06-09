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
    'name': 'Invoice Details In Sale And Purchase',
    'category': 'sale',
    'version': '18.0.0.0',
    'summary': 'This module provides invoice details in sale and purchase.',
    'website': ' ',
    'author': 'Sitaram',
    "license": "OPL-1",
    'description': 'This module provides invoice details in sale and purchase.',
    'depends': ['base', 'sale_management', 'purchase'],
    'data': [
        'views/sale_view.xml',
        'views/purchase_view.xml'
    ],
    'images': ['static/description/banner.png'],
    'live_test_url':'https://www.youtube.com/watch?v=66AffpP3ccc&feature=youtu.be',
    'auto_install': False,
    'installable': True,
    'application': False,
}
