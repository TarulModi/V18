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
    'name': 'Mass Confirm Sales Quotation and Send Email',
    'version': '18.0.0.0',
    'category': 'sales Management',
    "license": "OPL-1",
    'summary': 'This module use to select quotation and confirm it from tree view. You can also send quotation mail for the selected quotations',
    'description': """
        This module use to select quotation and confirm it from tree view. You can also send quotation mail for the selected quotations
        mass confirm sales quotations
        mass confirm sales order
        mass send quotation mail
        mass confirm so
        so mass confirm
        quotation mass confirmation
        easy to confirm multiple quotation
        multiple send by email quotations
        mass send email
        mass confirm quotations and send emails
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base','sale_management'],
    'data': [
            'security/ir.model.access.csv',
             'views/sr_mass_confirm_quotation.xml',
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.youtube.com/watch?v=ym7k2fObd3c',
    "images":['static/description/banner.png'],
}
