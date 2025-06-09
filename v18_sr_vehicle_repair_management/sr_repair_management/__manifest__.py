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
    'name': "Vehicle Repair Management",
    'version': "18.0",
    'summary': "Vehicle Repair Management",
    'category': 'Hidden',
    'description': """
    Vehicle Repair Management
    """,
    'author': "Sitaram",
    'website':"https://www.sitaramsolutions.in",
    'depends': ['base', 'account', 'mail', 'sale_management', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/vehicle_security.xml',
        'data/sequence.xml',
        'views/inherit_res_config_settings_view.xml',
        'views/vehicle_repair_menu.xml',
        'views/vehicle_repair_order.xml',
        'views/repair_diagnosis.xml',
        'views/repair_work_order.xml',
        'wizards/assign_technician_wizard_view.xml',
        'reports/report_diagnosis_repair.xml',
        'reports/report_diagnosis_repair_template.xml',
        'reports/report_estimate.xml',
        'reports/report_estimate_template.xml',
        'reports/report_repair_work_order.xml',
        'reports/report_repair_work_order_template.xml',
        'reports/report_vehicle_repair.xml',
        'reports/report_vehicle_repair_template.xml',
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
