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


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    code = fields.Char(string='Product Code')

    @api.onchange('product_id')
    def _onchange_product_template_code(self):
        if self.product_id and self.move_id.partner_id:
            customer = self.move_id.partner_id

            customer_code = self.env['product.customer.code'].search([
                ('product_variant_id', '=', self.product_id.id),
                ('customer_id', '=', customer.id),
            ])

            if customer_code:
                self.price_unit = self.product_id.list_price
                self.code = customer_code.code
            else:
                self.code = False