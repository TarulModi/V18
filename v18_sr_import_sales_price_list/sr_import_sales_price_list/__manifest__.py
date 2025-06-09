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
    'name': 'Import Sale PriceList',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Import Sales Price List using CSV, XLSX file',
    'description': 'Using this module we can import Sales Price List by searching'
                   ' the products in diffrent ways in csv or xlsx files',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_sales_price_list.xml'
    ],
    'author' : "Sitaram",
    'website':"https://sitaramsolutions.in",
    'installable': True,
    'auto_install': False,
    'application': False,
}
