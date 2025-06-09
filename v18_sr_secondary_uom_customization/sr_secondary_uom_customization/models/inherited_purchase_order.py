# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        if self.picking_ids:
            for picking in self.picking_ids:
                if picking.move_ids_without_package:
                    for move in picking.move_ids_without_package:
                        move.secondary_qty = move.purchase_line_id.secondary_qty
                        if move.move_line_ids:
                            for line in move.move_line_ids:
                                line.secondary_qty = line.move_id.secondary_qty
        return result

    def action_create_invoice(self):
        result = super(PurchaseOrder, self).action_create_invoice()
        if self.invoice_ids:
            for invoice in self.invoice_ids:
                if invoice.state == 'draft' and invoice.invoice_line_ids:
                    for line in invoice.invoice_line_ids:
                        if line.purchase_line_id:
                            line.secondary_qty = line.purchase_line_id.secondary_qty
        return result
