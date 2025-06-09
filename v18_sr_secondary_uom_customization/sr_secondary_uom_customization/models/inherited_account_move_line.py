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


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary')
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")

    _sql_constraints = [
        ('check_secondary_qty_positive',
         'CHECK(secondary_qty >= 0)',
         'Secondary quantity must be a non-negative value.')
    ]

    @api.onchange('quantity', 'product_id')
    def _onchange_quantity(self):
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.quantity
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.quantity
