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
    'name': "Purchase Multi Pickings",
    'version': "18.0.0.0",
    'summary': "This module allows you to create separate shipment per Purchase order line.",
    'category': 'Purchases',
    'description': """
        This module allows you to create separate shipment per Purchase order line.
        purchase multi shipment
        purchase multi pickings
        different shipment by purchase order lines
        different shipment by purchase lines
        separate shipment by purchase order lines
        separate shipment by purchase order
        separate picking by purchase order lines
        separate picking by purchase order
    """,
    'author': "Sitaram",
    'website': " ",
    'depends': ['base', 'purchase'],
    'data': [
        'views/purchase.xml'
    ],
    'demo': [],
    "license": "OPL-1",
    'images': ['static/description/banner.png'],
    'live_test_url': 'https://youtu.be/6pql7VwPPjo',
    'installable': True,
    'application': True,
    'auto_install': False,
}
