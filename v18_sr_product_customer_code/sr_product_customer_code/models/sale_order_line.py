# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    code = fields.Char(string='Product Code')

    @api.onchange('product_template_id')
    def _onchange_product_template_code(self):
        if self.product_template_id and self.order_id.partner_id:
            customer = self.order_id.partner_id

            customer_code = self.env['product.customer.code'].search([
                ('product_template_id', '=', self.product_template_id.id),
                ('customer_id', '=', customer.id),
            ], limit=1)

            if customer_code:
                self.product_uom_qty = 1
                self.price_unit = self.product_template_id.list_price
                self.code = customer_code.code
            else:
                self.code = False