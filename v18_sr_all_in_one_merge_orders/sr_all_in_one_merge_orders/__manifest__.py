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
    "name": "All In One Merge Orders | Merge Sales Quotations | Merge Purchase Quotations | Merge Customer Invoice | Merge Vendor Bills",
    "version": "18.0.0.0",
    "category": "Extra Addons",
    "license": "OPL-1",
    "summary": "Merge Customer Invoices merge vendor bills merge customer refund merge vendor refund merge same partner invoices merge same vendor bills merge rfq request for quotations merge with different options merge request for quotations in new quotations and existing quotations Merge Purchase quotations merge Purchase orders merge orders merge same partner Purchase quotations merge same state Purchase quotations Merge sales quotations merge sales orders merge orders merge same partner sales quotations merge same state sales quotations",
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
Merge quotations
Purchase quotations merge
merge Purchase quotations
merge same partner Purchase quotations 
merge same partner Purchase order
merge duplicate Purchase quotations
merge duplicate Purchase orders
merge multiple Purchase quotations to one Purchase quotations
merge multiple Purchase orders to one Purchase orders
merge Purchase quotations and cancel selected
merge Purchase quotations and delete selected
merge Purchase quotations in new Purchase quotations
merge Purchase quotations in existing Purchase quotations
merge Purchase orders and cancel selected
merge Purchase orders and delete selected
merge Purchase orders in new Purchase orders
merge Purchase orders in existing Purchase orders
combine Purchase quotations to one Purchase quotations
remove duplicate Purchase quotations
inherit purchase.order
merge Purchase order options
merge Purchase quotation options
merge rfq
request for quotations merge with different options
merge request for quotations in new quotations and existing quotations
Merge quotations
sales quotations merge
vendor sales orders
merge sales quotations
merge same partner quotations 
merge same partner sales order
merge duplicate quotations
merge duplicate sales orders
merge multiple sales quotations to one sales quotations
merge multiple sales orders to one sales orders
merge sales quotations and cancel selected
merge sales quotations and delete selected
merge sales quotations in new sales quotations
merge sales quotations in existing sales quotations
merge sales orders and cancel selected
merge sales orders and delete selected
merge sales orders in new sales orders
merge sales orders in existing sales orders
combine sales quotations to one quotations
remove duplicate quotations
inherit sale.order
merge sales order options
merge sales quotation options
""",
    "price": 40,
    "currency": "EUR",
    "author": "Sitaram",
    "depends": ["account", "sale_management", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/merge_invoice_customer_vendor_bills_view.xml",
        "wizard/merge_purchase_order_quotation_view.xml",
        "wizard/merge_sale_order_quotation_view.xml",
    ],
    "website": "https://sitaramsolutions.in",
    "installable": True,
    "auto_install": False,
    "live_test_url": "https://youtu.be/aCjj_RRvihs",
    "images": ["static/description/banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
