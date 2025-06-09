# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    shipping_length = fields.Float('Shipping Length')
    shipping_width = fields.Float('Shipping Width')
    shipping_height = fields.Float('Shipping Height')
    shipping_uom = fields.Many2one('uom.uom', string="Shipping unit")
    shipping_weight_uom = fields.Many2one('uom.uom', string="Shipping weight unit")
    listing_mirror_id = fields.Char(string="Listing Mirror Id")
