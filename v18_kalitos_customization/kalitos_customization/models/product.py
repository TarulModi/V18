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
from odoo.tools.misc import unique


class ProductVariant(models.Model):
    _inherit = 'product.product'

    extra_variant_price = fields.Float('Extra Price')

    @api.depends('list_price', 'price_extra', 'extra_variant_price')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        super(ProductVariant, self)._compute_product_lst_price()
        for product in self:
            product.lst_price += product.extra_variant_price

    @api.onchange('lst_price')
    def _set_product_lst_price(self):
        for product in self:
            product.write({'list_price': product.list_price - product.extra_variant_price})
