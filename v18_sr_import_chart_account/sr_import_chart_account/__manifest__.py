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
    'name': "Import Chart of Accounts using Excel or CSV",
    'version': "18.0.0.0",
    'summary': "This module helps you to import chart of accounts",
    'category': 'Accounting',
    'description': """
        Using this module Charts of Accounts is imported using excel sheets or CSV
    import charts of accounting using excel
    import charts of accounting using csv
    import charts of accounting using xls
    import charts of accounting using xlsx    
    localization
    import coa using excel
    import coa using csv
    import coa using xls
    import coa using xlsx
    import accounts using excel
    import accounts using csv
    import accounts using xls
    import accounts using xlsx
    import bulk chart of accounts
    """,
    'author': "Sitaram",
    'website':"sitaramsolutions.in",
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_coa.xml',
        
    ],
    'live_test_url':'https://youtu.be/IldArlHjeT8',
    'images': ['static/description/banner.png'],
    "price": 10,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
