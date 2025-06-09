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
    'name': 'Customer Supplier RMA',
    'version': '18.0.0.0',
    'category': 'Sales',
    "license": "OPL-1",
    'summary': 'Customer Supplier RMA',
    'description': """

""",
    'author': 'Sitaram',
    'depends': ['base','sale_management', 'stock', 'mail', 'purchase', 'account'],
    "data": [
        "security/ir.model.access.csv",
        "security/supplier_rma_security.xml",
        "data/ir_sequence_data.xml",
        "views/res_config_settings_view.xml",
        "views/reject_reason_view.xml",
        "views/rma_order_view.xml",
        "views/return_and_no_return_view.xml",
        "views/rma_supplier_view.xml",
        "views/rma_supplier_reason_view.xml",
        "wizard/return_refund_replace_view.xml",
        "wizard/supplier_create_reject.xml",
        "wizard/supplier_replace_product_view.xml",
        "views/stock_picking_view.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "report/report_rma_supplier.xml",
        "report/rma_supplier_report_template.xml",
        "report/report_rma_order.xml",
        "report/rma_order_report_template.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
