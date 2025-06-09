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
    'name': 'Sales Customization',
    'version': '18.0.0.0',
    'category': 'Sales',
    "license": "OPL-1",
    'summary': 'Sales Customization',
    'description': """

""",
    'author': 'Sitaram',
    'depends': ['sale_management', 'stock', 'purchase', 'account_accountant'],
    "data": [
            "security/ir.model.access.csv",
            "views/res_partner_view.xml",
            "views/res_config_settings_view.xml",
            "views/insufficient_stock_email_template.xml",
            "views/stock_picking_view.xml",
            "views/sale_order_view.xml",
            "views/purchase_order_view.xml",
            "wizard/sr_split_transfer_view.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
