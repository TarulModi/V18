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
    'name': 'Product Low Stock Notification',
    'version': '18.0.0.0',
    'category': 'Inventory',
    "license": "OPL-1",
    'summary': 'The Product Low Stock Notification is an Odoo application that helps you keep track of your inventory levels and ensures that you never run out of stock.',
    'description': """
    The Product Low Stock Notification is an Odoo application that helps you keep track of your inventory levels and ensures that you never run out of stock.
    This application works by sending you an email notification when the stock level of a particular product falls below a pre-defined threshold. This way, you can take immediate action and reorder the product before it runs out completely.
    sitaram solutions developed an application that gives you notification for the low product stock
    alert about low product stock
    product low stock notification
    odoo inventory
    inventory management
    manage inventory effectively
    Get notified via email when your product inventory falls below a certain threshold.
    Keep your inventory levels in check with automatic low stock notifications.
    Never run out of stock again with real-time notifications when your product inventory is running low.
    Stay on top of your inventory management with personalized low stock alerts.
    Proactively manage your inventory levels with automatic email notifications for low stock products.
    Get instant alerts when inventory levels are running low.
    Never run out of stock again with low stock notifications.
    Streamline your inventory management with automated low stock alerts.
    Take control of your inventory with timely low stock notifications.
    Stay on top of inventory levels and avoid stockouts with low stock alerts.
    Proactively manage inventory with real-time low stock notifications.
    Keep your operations running smoothly with low stock email notifications.
    Never miss a low stock situation again with automatic notifications.
    Receive timely alerts when inventory levels are getting low.
    Efficiently manage your inventory with low stock notifications by email.
    Stay on top of inventory levels with automatic low stock notifications.
    Effortlessly manage inventory levels with low stock email notifications.
    Keep your inventory optimized with customizable low stock notifications.
    Take proactive action to avoid stockouts with automated low stock alerts.
""",
    "price": 10,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['base','product','stock','mail'],
    'data': [
            'data/ir_cron_data.xml',
            'data/mail_template_data.xml',
            'views/product.xml',
            'views/res_config_settings.xml',
    ],
    'website':'https://www.sitaramsolutions.in',
    'application': True,
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/r7tH9iNRpms',
    "images":['static/description/banner.png'],
}
