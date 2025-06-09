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
    "name": "Merge Purchase Quotations (RFQ) In Odoo",
    "version": "18.0.0.0",
    "category": "Purchase",
    "license": "OPL-1",
    "summary": "merge rfq request for quotations merge with different options merge request for quotations in new quotations and existing quotations Merge Purchase quotations merge Purchase orders merge orders merge same partner Purchase quotations merge same state Purchase quotations",
    "description": """
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
 """,
    "price": 20,
    "currency": "EUR",
    "author": "Sitaram",
    "depends": ["purchase"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/merge_purchase_order_quotation_view.xml",
    ],
    "website": "https://sitaramsolutions.in",
    "installable": True,
    "auto_install": False,
    "live_test_url": "https://youtu.be/l7MurPrThdE",
    "images": ["static/description/banner.png"],
}
