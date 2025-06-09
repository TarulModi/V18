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
    "name": "All in One Mass/Bulk Duplicate Sales Orders, Purchase Orders And Invoices",
    'version': '18.0.0.0',
    'category': 'Extra Addons',
    "license": "OPL-1",
    'summary': 'All in One Mass/Bulk Duplicate Sales Order, Purchase Orders And Invoices',
    "description": """
        All in One Mass/Bulk Duplicate Sales Order, Purchase Orders And Invoices
        mass duplicate sales orders
        bulk duplicate sales order
        mass duplicate purchase orders
        bulk duplicate purchase orders
        mass duplicate invoices
        mass duplicate bills
        bulk duplicate invoices
        bulk duplicate bills
        multiple duplicate sales order
        multiple duplicate purchase order
        multiple duplicate invoices
        multiple duplicate bills
        
    """,
    "depends": ["base", "sale_management",'account','purchase'],
    "data": [
        "security/ir.model.access.csv",
        "wizard/sr_mass_duplicate_sales_order.xml",
        "wizard/sr_mass_duplicate_invoices.xml",
        "wizard/sr_mass_duplicate_purchase_order.xml",
    ],
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'installable': True,
    'auto_install': False,
    'website':'https://www.sitaramsolutions.in',
    'live_test_url':'https://www.sitaramsolutions.in',
    "images":['static/description/banner.png'],
}
