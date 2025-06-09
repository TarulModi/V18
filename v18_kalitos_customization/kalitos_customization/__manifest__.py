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
    'name': 'Kalitos - Customization',
    'version': '18.0',
    'category': 'Sales',
    "license": "OPL-1",
    'summary': 'Module for managing Variant Price',
    'description': """
        Manage Variant Extra Price    
""",
    'author': 'Sitaram',
    'depends': ['sale_management'],
    "data": [
            "views/product_view.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
