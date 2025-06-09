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
    'name': 'Payment Information In Invoice Report',
    'version': '18.0.0.0',
    'category': 'Accounting & Finance',
    'summary': 'This module used to show payment information in invoice report.',
    "license": "OPL-1",
    'description': """
        This module used to show payment information in invoice report.
""",
    'author': 'Sitaram',
    'depends': ['base','account'],
    'data': [
             'views/inherit_invoice_report.xml',
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/EYamS25yrwU',
    "images":['static/description/banner.png'],
    'website': "www.sitaramsolutions.in",
}
