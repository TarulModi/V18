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
    'name': "Import Projects",
    'version': "18.0.0.1",
    'summary': "This module helps you to import Projects",
    'category': 'Inventory/Inventory',
    'description': """
        Using this module Projects is imported using excel sheets
    import stock projects
    """,
    'author': "Sitaram",
    'website':"https://sitaramsolutions.in",
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_project_view.xml',
    ],
    'live_test_url':'https://youtu.be/q8-um-wX7tI',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
