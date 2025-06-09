# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _


class StockValuationLayer(models.Model):
    _inherit = "stock.valuation.layer"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary')
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")
