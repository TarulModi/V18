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
    "name": "Stock Picking Cancel",
    "version": "18.0.0.0",
    "summary": "This module used to Cancel Incoming and Outgoing Shipment/picking cancel order cancel shipment reverse movement reverse stock move reverse stock inventory",
    "category": "Warehouse",
    "description": """
	Tags:
        picking cancel, cancel order, cancel shipment, cancel transfers, 
        Cancel picking , cancel orders, cancel delivery order,
        cancel stock moves, cancel stock quants
	cancel stock picking
	cancel incoming shipment
	cancel outgoing shipment
	cancel internal shipment
	cancel stock
	cancel delivery
	cancel shipment
	revert shipment
	revert delivery
	odoo apps will help you to cancel picking, and shipment after done state in odoo
	Odoo cancel picking
	Odoo cancel incoming shipment
	odoo cancel outgoing shipment
	Cancel & Reset Picking
	Cancel Delivery Orders
	Stock Picking Cancel
	cancel picking and reverse stock
	reset to draft picking
	reverse stock movement
	reverse stock inventory
	cancel picking even after done state
	cancel picking even after deliver shipment
	cancel picking even after received shipment
    """,
    "author": "Sitaram",
    "website": "https://sitaramsolutions.in",
    "depends": ["base", "stock", 'stock_account'],
    "data": ["views/inherited_stock_picking.xml"],
    "live_test_url": "https://youtu.be/LIeYgUzo5DE",
    "images": ["static/description/banner.png"],
    "price": 10,
    "currency": "EUR",
    "demo": [],
    "license": "OPL-1",
    "installable": True,
    "auto_install": False,
}
