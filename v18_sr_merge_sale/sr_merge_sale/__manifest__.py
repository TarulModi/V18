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
    "name": "Merge Sales Quotations In Odoo",
    "version": "18.0.0.0",
    "category": "Sales",
    "license": "OPL-1",
    "summary": "Merge sales quotations merge sales orders merge orders merge same partner sales quotations merge same state sales quotations",
    "description": """
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
    "price": 20,
    "currency": "EUR",
    "author": "Sitaram",
    "depends": ["sale_management"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/merge_sale_order_quotation_view.xml",
    ],
    "website": "https://sitaramsolutions.in",
    "installable": True,
    "auto_install": False,
    "live_test_url": "https://youtu.be/UKdTdMcJDIo",
    "images": ["static/description/banner.png"],
}
