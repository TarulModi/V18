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
    'name': "Import Attendance from excel and CSV",
    'version': "18.0.0.0",
    'summary': "This module will help you to import attendance from excel and csv",
    'category': 'Attendances',
    'description': """
    Import employee attendance
    import attendances
    import attendance from excel
    import attendance from csv
    employee attendance
    employee presence
    employee sign in 
    employee sign out 
    import employee sign in
    import employee sing out
    import attendance data
    import attendance from old legacy erp to odoo
    import attendance from old odoo version to newer odoo version
    import attendance from other erp to odoo
    import attendance from biometric device to odoo via excel
    import attendance from biometric device to odoo via csv
    import attendance from finger print  device to odoo via excel
    import attendance from finger print  device to odoo via csv
    """,
    'author': "Sitaram",
    'website':"https://sitaramsolutions.in",
    'depends': ['base', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/sr_import_attendance_wizard.xml',
        'views/sr_import_attendance_menu.xml',
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
