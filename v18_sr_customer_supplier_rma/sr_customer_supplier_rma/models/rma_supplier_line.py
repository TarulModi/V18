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
from odoo.exceptions import ValidationError


class rmaSupplierLine(models.Model):
    _name = 'rma.supplier.line'
    _description = 'RMA Supplier Line'

    rma_supplier_id = fields.Many2one("rma.supplier", string="RMA Supplier")
    product_id = fields.Many2one('product.product', string="Product", readonly=True, store=True)
    price = fields.Float('Price')
    delivery_qty = fields.Float('Delivery Quantity')
    return_qty = fields.Float('Return Quantity')
    reason_id = fields.Many2one('rma.supplier.reason', string='Reason')
    purchase_line_id = fields.Many2one('purchase.order.line', string="Purchase Line", copy=False)
    reason_action = fields.Selection(related="reason_id.reason_action")
    received_qty = fields.Float('Received Quantity')
    stored_boolean = fields.Boolean("Stored Boolean", copy=False)

    # Replace
    replaced_product_id = fields.Many2one("product.product")
    replaced_qty = fields.Float("QTY")
    replaced_is_invoice = fields.Boolean("Create Invoice")

    @api.onchange("delivery_qty", "return_qty")
    def onchange_delivery_return_qty(self):
        if self.return_qty > self.delivery_qty:
            raise ValidationError(_("Return quantity should be less or equal to delivery quantity."))

    def open_replace_product(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'sr_customer_supplier_rma.action_supplier_replace_product')
        return action

    @api.onchange('reason_id')
    def onchange_reason_id(self):
        if self.reason_id and self.reason_id.reason_action == 'replace':
            self.stored_boolean = True
        else:
            self.stored_boolean = False
