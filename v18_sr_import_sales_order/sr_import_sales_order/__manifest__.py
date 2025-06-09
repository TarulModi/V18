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
    'name': "Import Sales Order",
    'version': "18.0.0.1",
    'summary': "This module helps you to import Sales Order/Quotations",
    'category': 'Sales',
    'description': """
        Using this module Sales Order/Quotations is imported using excel sheets
    import sales orders
    import quotations
    Import Quotations with Product Code
    Import Quotations with Product Name
    Import Quotations with Product Barcode.
    Import Quotations with Custom Sequence
    Import Quotations with Default System Sequence
    Import sales Orders with Product Code
    Import sales Orders with Product Name
    Import sales Orders with Product Barcode.
    Import sales Orders with Custom Sequence
    Import sales Orders with Default System Sequence
    Support Excel and CSV file
    Support Different warning
    easy import csv
    easy import excel
    import sales quotations from excel file
    import sales quotations from csv file
    migrate sales data from other erp to odoo
    migrate sales quotations from other erp to odoo
    migrate sales quotations from old legacy system to odoo
    migrate sales quotations from older version to newer version of odoo
    import sales order from excel file
    import sales order from csv file
    migrate sales order from other erp to odoo
    migrate sales order from old legacy system to odoo
    migrate sales order from older version to newer version of odoo
    """,
    'author': "Sitaram",
    'website':"https://sitaramsolutions.in",
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_sale_order.xml',
        
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
