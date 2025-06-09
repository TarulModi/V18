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
    'name': 'Hide Product Price',
    'version': '0.1',
    'category': 'Sales',
    'summary': 'This module allows you to hide cost price from product.',
    "license": "OPL-1",
    'website':"http://www.sitaramsolutions.in",
    'description': """
        This module allows you to hide cost price from product.
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base','product'],
    'data': [
             'security/product_security.xml',
             'views/product.xml'
    ],
    'installable': True,
    'live_test_url':'https://www.youtube.com/watch?v=PFk1Pf6MFpw&feature=youtu.be',
    'auto_install': False,
    "images":['static/description/banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
