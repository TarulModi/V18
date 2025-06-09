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
    'name': "Merge Stock picking",
    'version': "18.0.0.0",
    'summary': "",
    'category': 'Inventory',
    'description': """
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base','stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/merge_stock_picking_view.xml',
    ],
    'demo': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
