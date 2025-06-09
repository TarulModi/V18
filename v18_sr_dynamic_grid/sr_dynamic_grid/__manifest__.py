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
    'name': 'Dynamic Grid',
    'version': '18.0',
    'category': 'Tools',
    "license": "OPL-1",
    'summary': 'Dynamic Grid',
    'description': """
""",
    'author': 'Sitaram',
    'depends': ['web', 'base'],
    "data": [
            'security/ir.model.access.csv'
    ],
    "assets": {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
            'sr_dynamic_grid/static/src/css/*',
            'sr_dynamic_grid/static/src/xml/*',
            'sr_dynamic_grid/static/src/js/*',
        ],
    },
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
