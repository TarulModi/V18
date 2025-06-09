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
    'name': 'Sale test Order Duration Filter',
    'category': 'sale',
    'version': '18.0.0.0',
    'summary': 'This module provides duration filter to the sales order and sales quotation.',
    'website': ' ',
    'author': 'Sitaram',
    "license": "OPL-1",
    'description': 'This module provides duration filter to the sales order and sales quotation.',
    'depends': ['base', 'sale_management'],
    'data': [
        'views/sale_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'auto_install': False,
    'installable': True,
    'application': False,
}
