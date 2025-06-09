# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_order_line_id = fields.Many2one('sale.order.line')
    brand_id = fields.Many2one('product.brand', "Brand")
