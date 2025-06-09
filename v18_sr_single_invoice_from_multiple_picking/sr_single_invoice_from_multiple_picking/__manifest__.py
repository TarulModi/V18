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
    'name': "Create Single Invoice From Multiple Picking",
    'version': "18.0.0.0",
    'summary': "This module allows you to create single invoice from multiple picking",
    'category': 'Invoicing Management',
    'description': """
    Create single invoice from multiple pickings
    Create single customer invoice from multiple delivery picking
    Create single vendor invoice from multiple incoming picking
    Create single vendor invoice from purchase picking
    Create single customer invoice from outgoing delivery picking
    Generate single invoice from pickings
    Generate single customer invoice from delivery orders
    Generate single customer invoice from outgoing picking
    Generate single vendor invoice from incoming picking
    generate single customer invoice
    generate single vendor bill
    generate single supplier invoice
    generate single vendor invoice
    multiple picking generate single invoice
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'sale_management','stock','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_generate_single_invoice.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/yc7-sE_35_I',
    'images': ['static/description/banner.png'],
    "price": 15,
    "currency": 'EUR',
}
