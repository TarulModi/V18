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


class ProductBrandLine(models.Model):
    _name = 'product.brand.line'
    _description = 'Product Brand Line'

    product_id = fields.Many2one('product.product', 'Product')
    brand_id = fields.Many2one("product.brand", "Brand")
    brand_code = fields.Char("Brand SKU Code")
    mrp = fields.Float("MRP")
