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
    'name': 'Stock Inventory Turnover Analysis Report',
    'version': '18.0.0.0',
    'category': 'Inventory',
    "license": "OPL-1",
    'summary': 'odoo apps for stock inventory turnover report based on date, product, category, warehouses and company.',
    'description': """
    Tags:
        stock turnover, inventory turnover, inventory cycle, stock sale purchase cycle, 
        turnover analysis report, stock turnover analysis report, inventory turnover analysis report, inventory cycle analysis report, excel report, pdf report,
            with the help of this application you can export stock inventory turnover analysis report in excel format and pdf format.
        Sitaram Solutions stock inventory turnover analysis report application odoo module
        stock inventory
        stock inventory turnover report
        inventory anaylsis report by date range
        inventory analysis report by products
        inventory analysis report by product category
        inventory analysis report by warehouse
        inventory analysis report by company
        stock analysis report by date range
        stock analysis report by products
        stock analysis report by product category
        stock analysis report by product category
        stock analysis report by warehouse
        stock analysis report by company
        stock analysis cycle
        inventory analysis cycle
        stock turnover analysis excel report
        stock turnover analysis pdf report
        inventory turnover analysis excel report
        inventory turnover analysis pdf report
        stock analysis cycle excel report
        stock analysis cycle pdf report
        inventory cycle analysis excel report
        inventory cycle analysis pdf report
""",
    "price": 20,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'report/sr_stock_inventory_turnover_report_templates.xml',
        'views/sr_inventory_turnover_report_menu.xml',
        'wizard/sr_stock_inventory_turnover_report_view.xml'
    ],
    'website': 'https://www.sitaramsolutions.in',
    'application': False,
    'installable': True,
    'auto_install': False,
    'live_test_url': 'https://youtu.be/x18dGYu2Xqw',
    "images": ['static/description/banner.png'],
}
