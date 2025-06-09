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
    'name': 'Automotive Part Order and Customization',
    'version': '18.0.0.0',
    'category': 'Fleet',
    "license": "OPL-1",
    'summary': 'Module for managing automotive part ordering, customization, and fleet integration',
    'description': """
        This module facilitates the seamless ordering and customization of automotive parts. It enables:
        Management of automotive parts and their suppliers.
        Integration with fleet vehicles and body types.
        Enhanced sales and purchase order processing for automotive businesses.
        Customizable views for product brands, fleet types, and partner management.
        Import master table
        Import Contacts
        Import Fleet Vehicle
        Import Product
        Import Product Stock
        Whatsapp template for Garage on Sales order
        Whatsapp template for vendor on Purchase order
        Manage Fleet Vehicle process
        Manage Contact Process
        Mapping Product Variant with Fleet Vehicle
        Manage contacts based on Supplier, Garage, Owner & Compnay/Shop
        Manage Product Variant extra price        
""",
    'author': 'Sitaram',
    'depends': ['fleet', 'sale_management', 'stock', 'purchase', 'contacts'],
    "data": [
            "security/ir.model.access.csv",
            "views/fleet_vehicle_view.xml",
            "views/product_view.xml",
            "views/sale_order_view.xml",
            "views/fleet_generation_view.xml",
            "views/fleet_body_type_view.xml",
            "views/fleet_type_view.xml",
            "views/product_template_view.xml",
            "views/product_brand_view.xml",
            "views/product_suplierinfo_view.xml",
            "views/partner_cluster_view.xml",
            "views/res_partner_view.xml",
            "views/purchase_order_view.xml",
            "views/sale_cancel_reason_view.xml",
            "views/purchase_cancel_reason_view.xml",
            "views/fleet_variant_view.xml",
            "wizard/wizard_sale_line_po_views.xml",
            "wizard/sr_import_product_supplier.xml",
            "wizard/sr_remove_product_car_mapping.xml",
            "wizard/sr_remove_product_brand_mapping.xml",
            "wizard/sr_filter_sale_model_view.xml",
            "wizard/wizard_supplier_info_view.xml",
            "wizard/wizard_sale_cancel_reason_views.xml",
            "wizard/wizard_purchase_cancel_reason_views.xml",
            "wizard/sr_garage_whatsapp_template.xml",
            "wizard/sr_vendor_whatsapp_template.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'installable': True,
    'auto_install': False,
}
