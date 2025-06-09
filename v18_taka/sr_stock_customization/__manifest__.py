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
    'name': 'Inventory Customization',
    'version': '18.0.0.0',
    'category': 'Stock',
    "license": "OPL-1",
    'summary': 'Inventory Customization',
    'description': """
        
""",
    'author': 'Sitaram',
    'depends': ['stock'],
    "data": [
            "views/stock_picking_view.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
