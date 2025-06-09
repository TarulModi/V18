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
    'name': "Subscription Management",
    'version': "18.0.0.0",
    'summary': "Subscription management for selected object and records",
    'category': 'Extra Addons',
    'description': """
    subscription management
    create subscription record for selected object and record
    customer's subscription life cycle
    recurring record
    object recurring
    object subscription
    record subscription
    customer subscription
    vendor subscription
    recurring operation
    subscription operations
    scheduled operation
    scheduled process
    recurring process
    """,
    'author': "Sitaram",
    'website':"www.sitaramsolutions.in",
    'depends': ['base','sales_team','portal'],
    'data': [
        'data/ir_sequence_data.xml',
        'security/ir.model.access.csv',
        'views/sr_subscription_management_view.xml',
    ],
    'demo': [],
    "price": 20,
    "currency": 'EUR',
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/GXint5F2tcY',
    'images': ['static/description/banner.png'],
}
