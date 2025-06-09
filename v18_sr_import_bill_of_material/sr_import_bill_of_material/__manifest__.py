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
    'name': 'Import BOM',
    'version': '18.0.0.1',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Import Bill of materials using CSV, XLSX file',
    'description': 'Using this module we can import bom by searching'
                   ' the products in diffrent ways in csv or xlsx files',
    'depends': ['base', 'stock', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_bill_of_material.xml',
    ],
    'license': 'OPL-1',
    'author': 'Sitaram',
    'installable': True,
    'auto_install': False,
    'application': False,
}
