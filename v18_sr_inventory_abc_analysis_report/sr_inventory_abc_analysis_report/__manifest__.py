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
    "name": "ABC Analysis in Inventory Management",
    "version": "18.0.0.0",
    'category': 'Inventory',
    "license": "OPL-1",
    "summary": "The purpose of the report is to help businesses prioritize their inventory management efforts and make informed decisions about inventory replenishment, storage and monitoring.A list of the inventory items and their respective category (A, B, or C). An inventory ABC analysis report is a document that summarizes the results of an ABC analysis and provides information on the different categories of inventory items.",
    "description": """
        Inventory ABC analysis is a method used in inventory management to categorize inventory items into three categories (A, B, and C) based on their importance or impact on the overall business. The A items are considered the most important and are given the most attention, while the C items are considered the least important and are given the least attention.
        An inventory ABC analysis report is a document that summarizes the results of an ABC analysis and provides information on the different categories of inventory items.
        A list of the inventory items and their respective category (A, B, or C)
        The total value or cost of each category of inventory
        The percentage of total inventory value or cost that each category represents
        Recommendations for managing each category of inventory, such as frequency of review and reorder points
        ABC analysis helps to prioritize inventory items based on their importance, which can aid in decision making.
        By focusing on the most important items (category A), a company can reduce overall inventory costs while still maintaining an adequate supply of critical items.
        By understanding the sales patterns of category A items, a company can improve their forecasting accuracy and reduce stockouts.
        By focusing on the most important items, a company can better allocate their resources and improve their overall efficiency
        With ABC analysis, a company can establish better control over their inventory, reducing the risk of stockouts and overstocking.
        manage risk with maintaining inventory
        improve sales
        ABC analysis
        inventory control analysis
        control inventory with this abc analysis report
        sitaram solutions developed new application called ABC analysis report
        Inventory ABC analysis
        product ABC analysis
        Product category ABC analysis
        ABC analysis based on sold Units
        ABC analysis based on consumption value
        know your fast moving items in your inventory
        Identify value of your inventory
""",
    "price": 20,
    "currency": 'EUR',
    'author': 'Sitaram',
    'depends': ['web', 'stock','sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "report/sr_stock_inventory_abc_report_templates.xml",
        "wizard/sr_stock_inventory_abc_report_view.xml",
        "views/sr_stock_inventory_abc_report_menu.xml",
    ],
    'website':'https://www.sitaramsolutions.in',
    'application': True,
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/kNUH7g_kWNQ',
    "images":['static/description/banner.png'],
}
