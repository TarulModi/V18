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


class BOMLine(models.Model):
    _inherit = "mrp.bom.line"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary')
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")

    _sql_constraints = [
        ('check_secondary_qty_positive',
         'CHECK(secondary_qty >= 0)',
         'Secondary quantity must be a non-negative value.')
    ]

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = super(BOMLine, self).onchange_product_id()
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio
            else:
                self.secondary_qty = self.product_id.standard_ratio
        return result

    @api.onchange('product_qty')
    def onchange_product_qty(self):
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.product_qty
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.product_qty
