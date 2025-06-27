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
    'name' : 'sr Product Customer Code',
    'description' : 'sr Product Customer Code',
    'version' : '18.0.0.0',
    'depends' : ['base','product','sale_management'],
    'data' : [
        'security/ir.model.access.csv',
        'view/product_customer_code_view.xml',
        'view/product_product_view.xml',
        'view/product_template_view.xml',
        'view/sale_order_view.xml'
    ],
    'installable' : True,
    'application' : True,
    'license' : 'LGPL-3',
}