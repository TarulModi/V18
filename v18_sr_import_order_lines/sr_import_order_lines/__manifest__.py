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
    'name': "Import Order Lines - Sales Quotations | Purchase Quotations (RFQ) | Customer Invoice | Vendor Bills",
    'version': '18.0.0.0',
    'category': 'Extra Addons',
    "license": "OPL-1",
    'summary': "This module helps you to import order line of sales quotations, purchase quotations, customer invoice and vendor bills",
    'description': """
        Using this module order lines is imported using excel sheets
    import sales order lines from csv file
    import sales quotations lines from excel file
    import sales order line from excel file
    import sales quotations line from csv file
    import customer invoice lines from csv file
    import customer invoice lines from excel file
    import vendor bills line from excel file
    import vendor bills line from csv file
    import purchase order line from excel file
    import purchase order line from csv file
    import purchase quotation line from csv file
    import purchase quotation line from excel file
    import rfq line from excel file
    import rfq line from csv file
    import large number of lines in sales quotations from excel
    import large number of lines in sales quotations from csv
    import large number of lines in sales order from excel
    import large number of lines in sales order from csv
    import large number of lines in rfq from excel
    import large number of lines in purchase quotation from csv
    import large number of lines in rfq from csv
    import large number of lines in purchase quotation from excel
    import large number of lines in purchase orders from csv
    import large number of lines in purchase order from excel
    import large number of lines in customer invoice from csv
    import large number of lines in customer invoice from excel
    import large number of lines in vendor bill from csv
    import large number of lines in vendor bill from excel
    odoo import bulk Sales order line from excel file
    odoo import bulk Sales order line from csv file
    odoo import bulk Sales quotation line from Excel file
    odoo import bulk Sales quotation line from csv file
    odoo import bulk purchase order line from excel file
    odoo import bulk purchase order line from csv file
    odoo import bulk purchase quotation line from Excel file
    odoo import bulk purchase quotation line from csv file
    odoo import bulk rfq line from csv file
    odoo import bulk customer invoice line from csv file
    odoo import bulk vendor bills line from excel file
    inherit sale.order
    inherit acount.move
    inherit purchase.order
    """,
    "price": 20,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base', 'sale_management', 'sale', 'purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_sale_order_lines.xml',
        'wizard/sr_import_account_move_lines.xml',
        'wizard/sr_import_purchase_order_lines.xml',
        'views/inherited_sale_order.xml',
        'views/inherited_account_move.xml',
        'views/inherited_purchase_order.xml'
        
    ],
    'website':'https://sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/ary0V0Ei9CU',
    "images":['static/description/banner.png'],
}
