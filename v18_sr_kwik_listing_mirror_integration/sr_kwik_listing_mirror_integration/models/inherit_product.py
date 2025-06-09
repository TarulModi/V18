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


class ProductProduct(models.Model):
    _inherit = "product.product"

    asin = fields.Char('ASIN')
    upc = fields.Char('UPC')
    mpn = fields.Char('MPN')
    brand = fields.Char('Brand')
