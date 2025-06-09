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
    "name": "Merge Invoices (Customer Invoice/Vendor Bills/Refunds)",
    "version": "18.0.0.0",
    "category": "Accounting",
    "license": "OPL-1",
    "summary": "Merge Customer Invoices merge vendor bills merge customer refund merge vendor refund merge same partner invoices merge same vendor bills",
    "description": """
Merge Customer
Invoices merge
vendor bills
merge customer refund
merge vendor refund
merge same partner invoices 
merge same vendor bills
merge duplicate invoices
merge duplicate bills
merge multiple invoices to one invoice
merge multiple bills to one bills
merge multiple refunds to one refund
merge invoices and cancel selected
merge invoices and delete selected
merge invoice in new invoice
merge invoice in existing invoice
merge bills and cancel selected
merge bills and delete selected
merge bills in new bills
merge bills in existing bills
merge refund and cancel selected
merge refund and delete selected
merge refund in new refund
merge refund in existing refund
combine multiple invoice to one invoice
remove duplicate invoice
multi currency invoices
change currency of the invoices
inherit account.move
merge invoices options
""",
    "price": 20,
    "currency": "EUR",
    "author": "Sitaram",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/merge_invoice_customer_vendor_bills_view.xml",
    ],
    "website": "https://sitaramsolutions.in",
    "installable": True,
    "auto_install": False,
    "live_test_url": "https://youtu.be/mX-Zt9Qz8ss",
    "images": ["static/description/banner.png"],
}
