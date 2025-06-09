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
    'name': "Mass Mailing For Sale,Invoice,Purchase",
    'version': "18.0.0.0",
    'summary': "This module is used to send mass email to multiple customers or vendor for sale,invoice purchase.",
    'category': 'Extra Tools',
    "license": "OPL-1",
    "price": 30,
    "currency": 'EUR',
    'website':"https://www.sitaramsolutions.in",
    'description': """
    This module is used to send mass email to multiple customers or vendor for sale,invoice purchase.
    All In One Mass Mailing
    Mass Mailing
    sale mass mailing
    invoice mass mailing
    purchase mass mailing
    generic mass mailing
    send mail to customers
    send mail to the multiple customers at a time
    send mail to the vendors
    send mail to the multiple vendors at a time
    marketing
    send mass email
    invoice mail
    sales order email
    purchase order email
    rfq email
    request for quotations email
    """,
    'author': "Sitaram",
    'depends': ['base', 'sale_management','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_view.xml',
        'wizard/invoice_view.xml',
        'wizard/purchase_view.xml'
    ],
    'demo': [],
    'images':['static/description/banner.png'],
    'live_test_url':'https://www.youtube.com/watch?v=ulCSkG8YOH4&feature=youtu.be',
    'installable': True,
    'application': True,
    'auto_install': False,
}
