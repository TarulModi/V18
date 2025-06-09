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
    'name': 'Employee Offer Letter',
    'version': '18.0.0.0',
    'category': 'Human Resources',
    'summary': 'Print Offer Letter from Employee Form',
    'depends': ['hr'],
    'data': [
        'report/offer_letter_template.xml',
        'report/offer_letter_report.xml',
        'views/hr_employee_view.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
}
