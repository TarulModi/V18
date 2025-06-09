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
    'name': "Restrict out of Product Stocks in Sales Quotation",
    'version': "18.0.0.0",
    'summary': "This module will helps you to restrict users to confirm sales quotation if any product is not available in warehouse.",
    'category': 'Sales',
    'description': """
    out of stock restriction
    odoo restriction for out of stock
    can not proceed sales quotation if product is not available
    can not confirm sale quotation when product is not in stock
    out of stock functionality
    forbidden to confirm sales quotation is product not in stock
    odoo sale quotation warning
    out of stock warning
    odoo product stock
    odoo sale order stock
    odoo sale quotation stock check
    check product stock
    indicate red line if product not in stock
    odoo stock inventory
    odoo stock check
    unavailability of stock warning
    low stock warning
    """,
    'author': "Sitaram",
    'website':"www.sitaramsolutions.in",
    'depends': ['base','sale_management'],
    'data': [
        'views/sr_inherit_res_config_setting.xml',
        'views/sr_inherit_sale_order.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    "price": 10,
    "currency": 'EUR',
    'live_test_url':'https://youtu.be/_B5GPUvxutk',
    'images': ['static/description/banner.png'],
}
