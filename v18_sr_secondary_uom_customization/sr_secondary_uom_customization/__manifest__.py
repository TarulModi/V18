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
    "name": "Secondary UOM Customization",
    "version": "18.0",
    "category": "Sales/Sales",
    "summary": "Secondary UOM Customization",
    "description": """
        Secondary UOM Customization
    """,
    "author": "Sitaram",
    "depends": ["base", "stock", "sale_management", "account", "purchase", "stock_account", "mrp"],
    "data": [
        "data/secondary_data.xml",
        "views/inherited_product_template.xml",
        "views/inherited_product_product.xml",
        "views/inherited_account_move_view.xml",
        "views/inherited_purchase_order_view.xml",
        "views/inherited_sale_order_view.xml",
        "views/inherited_stock_move_view.xml",
        "views/inherited_stock_move_line_view.xml",
        "views/inherited_stock_quant_view.xml",
        "views/inherited_stock_valuation_layer_view.xml",
        "views/inherited_stock_picking_view.xml",
        "views/inherited_bom_view.xml",
        "views/inherited_manufacturing_view.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'sr_secondary_uom_customization/static/src/xml/custom_bom_overview_line.xml',
            'sr_secondary_uom_customization/static/src/xml/mrp_bom_overview_table.xml',
        ],
    },
    "website": "https://sitaramsolutions.in",
    "application": True,
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
}
