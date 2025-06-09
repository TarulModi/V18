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
    'name': "Import Partners(Customers/Vendors) and Products",
    'version': "18.0.0.0",
    'summary': "This module helps you to import Customers/Vendors and products",
    'category': 'Accounting',
    'description': """
        Using this module Partners and products is imported using excel sheets
    import customers using csv 
    import customers using xls
    import suppliers using csv 
    import suppliers using xls
    import products using csv 
    import products using xls
    import vendors using csv 
    import vendors using xls
    import customers using excel
    import Suppliers using excel
    import vendor using excel
    import products using excel
    import partners using csv 
    easy import customers
    easy import suppliers
    easy import vendors
    easy import products    
    """,
    'author': "Sitaram",
    'website':"www.sitaramsolutions.in",
    'depends': ['base', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sr_import_partner.xml',
        'wizard/sr_import_product.xml'
        
    ],
    'live_test_url':'https://youtu.be/EGBUDLPPibw',
    'images': ['static/description/banner.png'],
    "price": 20,
    "currency": 'EUR',
    'demo': [],
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
}
