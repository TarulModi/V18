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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    inv_amount = fields.Float('Invoice Amount', compute='_compute_invoice_values')
    inv_due_amount = fields.Float('Invoice Due Amount', compute='_compute_invoice_values')
    inv_paid_amount = fields.Float('Invoice Paid Amount', compute='_compute_invoice_values')

    @api.depends('invoice_ids', 'invoice_ids.amount_total', 'invoice_ids.amount_residual', 'invoice_ids.state')
    def _compute_invoice_values(self):
        for order in self:
            total = 0
            due = 0
            paid = 0
            for invoice in order.invoice_ids:
                total += invoice.amount_total
                if invoice.state != 'draft':
                    due += invoice.amount_residual
                    paid += invoice.amount_total - invoice.amount_residual
                else:
                    due += invoice.amount_total

            order.inv_amount = total
            order.inv_due_amount = due
            order.inv_paid_amount = paid
