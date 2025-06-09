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
    'name': "Import For Attendance"
            "Bill of Material"
            "Chart of Account"
            "CRM Lead"
            "Inventory Adjustment"
            "Invoice"
            "Import Journal Entry"
            "Order Lines - Sales Quotations | Purchase Quotations (RFQ) | Customer Invoice | Vendor Bills"
            "Partners(Customers/Vendors) and Products"
            "Projects"
            "Project Tasks"
            "Purchase Orders"
            "Sales Order"
            "Sale PriceList"
            "Stock Picking"
            "from excel and CSV",
    'version': "18.0.0.0",
    'summary': "This module will help you to imports all in one records from excel and csv",
    'category': 'Extra Addons',
    'description': """
    """,
    'author': "Sitaram",
    'website':"https://sitaramsolutions.in",
    'depends': ['base', 'hr_attendance', 'crm', 'account', 'stock', 'mrp', 'sale_management', 'sale', 'purchase', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/sr_import_attendance_wizard.xml',
        'wizards/sr_import_bill_of_material.xml',
        'wizards/sr_import_coa.xml',
        'wizards/import_crm_lead_view.xml',
        'wizards/sr_import_inventory_adjustment.xml',
        'wizards/sr_import_invoice.xml',
        'wizards/sr_import_journal_entry_view.xml',
        'wizards/sr_import_sale_order_lines.xml',
        'wizards/sr_import_account_move_lines.xml',
        'wizards/sr_import_purchase_order_lines.xml',
        'wizards/sr_import_partner.xml',
        'wizards/sr_import_product.xml',
        'wizards/sr_import_project_view.xml',
        'wizards/sr_import_project_task_view.xml',
        'wizards/import_purchase.xml',
        'wizards/sr_import_sale_order.xml',
        'wizards/sr_import_sales_price_list.xml',
        'wizards/sr_import_stock_picking_view.xml',
        'views/sr_import_attendance_menu.xml',
        'views/inherited_sale_order.xml',
        'views/inherited_account_move.xml',
        'views/inherited_purchase_order.xml',
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/KXhDYDq8kUo',
    'images': ['static/description/banner.png'],
    "price": 10,
    "currency": 'EUR',
    
}
