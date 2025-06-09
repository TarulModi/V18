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
    "name": "Employee Expense Limit",
    "version": "18.0.0.0",
    "category": "Human Resources/Expenses",
    "license": "OPL-1",
    'summary': 'Employee expense limit limit for expense',
    "description": """
        Employee Expense Limit
        limit for expense
        fix expense for employee
        employee limit exceed warning
        define limit for expense
        inherit hr.employee
        inherit product.product
        allocate expense limit
        allow limit for spend
    """,
    "depends": ["base", "hr", "product", "hr_expense"],
    "data": [
        "security/ir.model.access.csv",
        "views/inherited_product_view.xml",
    ],
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'installable': True,
    'auto_install': False,
    'website':'https://www.sitaramsolutions.in',
    'live_test_url':'https://www.sitaramsolutions.in',
    "images":['static/description/banner.png'],
}
