# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _create_invoices(self, sale_orders):
        invoice_id = super(SaleAdvancePaymentInv, self)._create_invoices(sale_orders)
        if invoice_id:
            for invoice in invoice_id:
                if invoice.state == 'draft' and invoice.invoice_line_ids:
                    for line in invoice.invoice_line_ids:
                        if line.sale_line_ids:
                            sum_secondary_qty = sum(line.sale_line_ids.mapped('secondary_qty'))
                            line.secondary_qty = sum_secondary_qty
        return invoice_id
