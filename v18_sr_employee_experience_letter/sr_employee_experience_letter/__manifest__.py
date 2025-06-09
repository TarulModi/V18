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
    'name': 'Employee Experience Letter',
    'version': '18.0.0.0',
    'category': 'Human Resources',
    'summary': 'Print Experience Letter from Employee Form',
    'depends': ['hr'],
    'data': [
        'report/experience_letter_template.xml',
        'report/experience_letter_report.xml',
        'views/hr_employee_inherit_view.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'OPL-1',
}
