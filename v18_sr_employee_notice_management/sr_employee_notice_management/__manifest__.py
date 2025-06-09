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
    'name': "Notice/Warning Management For Employee Behavior",
    'version': "18.0.0.0",
    'summary': "This module is used to  Manager to send notice regarding offense to employees.",
    'category': 'Extra Tools',
    'description': """
    offense of employee
    notice for offense
    manager can send notice to the employee
    office can send notice to the employee
    warnings
    Statutory Warning
    contractual notice
    higher management can send notice for employee behaviour
    unprofessional behavior
    hr Disciplinary warning 
    Employee Disciplinary Odoo App
    Employee Review
    Employee Offense notice 
    HR Employee Warning Letter
    Employee Warning
    Warning Letter
    hr Employee General Warning
    hr General Warning
    hr Behavior Warning
    hi warning
    warning for attitude
    attitude offense
    """,
    'author': "Sitaram",
    'website':"http://www.sitaramsolutions.in",
    'depends': ['base', 'hr', 'portal', 'utm'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/sr_notice_management_view.xml',
        'views/inherited_hr_employee.xml',
        'report/employee_notice_report.xml',
        'report/employee_notice_report_template.xml'
    ],
    'demo': [],
    "external_dependencies": {},
    "license": "OPL-1",
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/8NsENuEqxKI',
    'images': ['static/description/banner.png'],
    "price": 15,
    "currency": 'EUR',
}
