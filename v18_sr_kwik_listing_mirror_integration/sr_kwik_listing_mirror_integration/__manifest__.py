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
    'name': "Kwik Listing Mirror Integration",
    'version': "18.0",
    'summary': "Kwik Listing Mirror Integration",
    'category': 'Hidden',
    'description': """
    Kwik Listing Mirror Integration
    """,
    'author': "Sitaram",
    'website':"https://www.sitaramsolutions.in",
    'depends': ['base', 'sale_management', 'purchase', 'product', 'stock', 'mrp','stock_picking_batch','stock_barcode'],
    'data': [
        'security/ir.model.access.csv',
        'data/demo.xml',
        'data/cron.xml',
        'views/inherit_res_config_settings_view.xml',
        'views/listing_mirror_integration_view.xml',
        'views/inherit_res_partner_view.xml',
        'views/inherit_product_template_view.xml',
        'views/inherit_product_view.xml',
        'views/integration_error_log_view.xml',
        'views/inherited_sale_order.xml',
        'views/update_qty_log.xml',
        'views/inherit_stock_location_view.xml',
        'views/inherit_stock_quant_view.xml',
        'views/integration_log_details_view.xml',
        'wizards/update_product_listing_mirror_view.xml',
        'wizards/push_qty_to_listing_mirror_view.xml',
        'wizards/update_order_listing_mirror_view.xml',
    ],
    "license": "OPL-1",
    'application': True,
    'installable': True,
    'auto_install': False,
}
