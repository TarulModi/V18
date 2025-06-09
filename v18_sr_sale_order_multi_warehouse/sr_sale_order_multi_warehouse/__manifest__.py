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
    'name': 'Sales Order Multiple Warehouse',
    'version': '18.0.0.0',
    'category': 'Extra Addons',
    "license": "OPL-1",
    'summary': 'Warehouse Selection on Sale order line in Odoo.',
    'description': """
    This application will give you option to select warehouse in sale order line. Once you confirm the sales order it will create delivery orders based on given warehouse in sale order line. It will groupby same warehouse in one delivery orders automatically. You can see warehouse in sale order report also.
    multi shipment
    sale multiple delivery orders
    select warehouse in sale order line
    sale multiple shipment
    single sale order multiple delivery orders
    single sale order multiple shipment
    warehouse in sales report
    groupby warehouse in delivery orders
    delivery orders based on selected warehouse in sales order line
    multiple stock picking for single sale quotation
    multiple outgoing shipments based on selected warehouse in sales order
    stock manage from sales order line by selecting warehouse
    warehouse routing
    delivery routing
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'website':"https://sitaramsolutions.in",
    'depends': ['base','sale_management','sale','stock'],
    'data': [
             'views/sr_inherit_sale_order.xml',
             'report/inherit_sale_report_template.xml'
    ],
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/vfMJx4m7j2s',
    "images":['static/description/banner.png'],
}
