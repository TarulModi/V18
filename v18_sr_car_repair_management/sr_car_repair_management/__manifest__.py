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
    'name': "Car Repair Management",
    'version': "18.0",
    'summary': "Car Repair Management",
    'category': 'Hidden',
    'description': """
    Car Repair Management
    """,
    'author': "Sitaram",
    'website':"https://www.sitaramsolutions.in",
    'depends': ['base', 'account', 'mail', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'security/car_security.xml',
        'data/sequence.xml',
        'views/car_repair_menu.xml',
        'views/car_repair_form_view.xml',
        'views/car_diagnosis.xml',
        'wizards/assign_technician_wizard_view.xml',
        'reports/report_car_repair.xml',
        'reports/report_car_repair_template.xml'
    ],
    "license": "OPL-1",
    'application': True,
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.youtube.com/watch?v=P3GTFjzGtpY&t=102s',
    'images': ['static/description/banner.png'],
    "price": 50,
    "currency": 'EUR',
    
}
