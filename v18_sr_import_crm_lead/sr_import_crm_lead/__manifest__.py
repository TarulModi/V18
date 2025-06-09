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
    'name': "Import CRM Lead from Excel/CSV",
    'version': "18.0.0.1",
    'summary': "This module helps you to import CRM Lead from Excel/CSV",
    'category': 'Sales/CRM',
    'description': """
     Using this module CRM Lead is imported using excel/CSV sheets
    """,
    'author': "Sitaram",
    'website': "https://sitaramsolutions.in",
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_crm_lead_view.xml',
    ],
    'live_test_url':'https://youtu.be/fPgZYHlavXA',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
