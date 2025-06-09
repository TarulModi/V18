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
    'name': "Import Customer Invoices/Vendor Bills/ Customers  Refunds/ Vendors Refunds",
    'version': "18.0.0.1",
    'summary': "This module helps you to import Customer Invoices/Vendor Bills/ Customers  Refunds/ Vendors Refunds",
    'category': 'Accounting',
    'description': """
        Using this module Customer Invoices/Vendor Bills/ Customers  refunds/ Vendors Refunds is imported using excel sheets
    import customers Invoice using csv 
    import customers Invoice using xls
    import customers Refund using csv 
    import customers Refund using xls
    import Vendors Bills using csv 
    import Vendors Bills using xls
    import Vendors Refund using csv 
    import Vendors Refund using xls
    import with invoice state configuration
    import draft invoice
    import open invoice
    update invoice
    import with custom sequence
    import with default sequence
    import with product name/code/barcode
    import with customers/vendors name or reference code
    import custom account in invoice line
    import customer invoices from old legacy system to odoo
    import vendor bills from old odoo version to newer odoo version
    import vendor bills from old legacy system to odoo
    import customer invoices old odoo version to newer odoo version
    
    """,
    'author': "Sitaram",
    'website': "https://sitaramsolutions.in",
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_invoice.xml',
        
    ],
    'live_test_url':'https://youtu.be/RnAOUQMfc8M',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
