# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _

class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_code_ids = fields.One2many('product.customer.code', 'product_variant_id')

    x_customer_code_search = fields.Char(string='Customer Code', compute='compute_code',search='search_customer_code', store=False)

    def compute_code(self):
        for rec in self:
            rec.x_customer_code_search = ''

    def search_customer_code(self, operator, value):
        if not value:
            return []
        product_codes = self.env['product.customer.code'].search([('code', operator, value)])
        template_ids = product_codes.mapped('product_variant_id').ids
        return [('id', 'in', template_ids)]