# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models

class ProductProduct(models.Model):
    _inherit = 'product.product'

    invoice_count = fields.Float(string='Invoice Qty', compute='_compute_invoice_stats', store=True)
    invoice_amount_count = fields.Float(string='Invoice Amount', compute='_compute_invoice_stats', store=True)

    @api.depends('invoice_count', 'invoice_amount_count')
    def _compute_invoice_stats(self):
        for product in self:
            domain = [
                ('move_id.state', 'in', ['posted', 'paid']),
                ('product_id', '=', product.id),
            ]
            invoice_lines = self.env['account.move.line'].search(domain)
            product.invoice_count = sum(line.quantity for line in invoice_lines)
            product.invoice_amount_count = sum(line.price_subtotal for line in invoice_lines)
