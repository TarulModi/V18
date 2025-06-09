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
    'name': 'Advance Payment For Sales and Purchase Order',
    'version': '18.0.0.0',
    'category': 'Extra Addons',
    "license": "OPL-1",
    'summary': 'Advance Payment for Sales And Purchase orders, sales payment, purchase payment, advance payment, register payment.',
    'description': """
    Sales Quotation advance payment
    Sales Order Advance Payment
    odoo Sales order quotation advance payment
    advance payment in odoo
    payment before generate invoice
    accept payment when create draft sales order
    give payment when create draft purchase order
    customer advance payment
    supplier advance payment
    vendor advance payment
    advance payment history on sales order
    advance payment history on purchase order
    you can register advance payment by this apps
    you can register advance payment for customer
    you can register advance payment for supplier vendors
    you can register advance payment for sales quotations
    you can register advance payment for purchase quotations
    maintain history of the advance payment
    maintain journal entry for advance payment
    generate journal entry for advance payment
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'website':"https://sitaramsolutions.in",
    'depends': ['base','sale_management','purchase'],
    'data': [
            'security/ir.model.access.csv',
             'views/sr_inherit_sale_order.xml',
             'views/sr_inherit_purchase_order.xml',
             'wizard/account_sale_advance_payment.xml',
             'wizard/account_purchase_advance_payment.xml'
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/w_cYaf52jeI',
    "images":['static/description/banner.png'],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
