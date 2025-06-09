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


class rmaOrderLine(models.Model):
    _name = 'rma.order.line'
    _description = 'RMA Order Line'
    _rec_name = 'product_id'
    _inherit = ['mail.thread']

    rma_order_id = fields.Many2one("rma.order")
    product_id = fields.Many2one('product.product', string="Product")
    return_id = fields.Many2one('return.no.return', string="Return/NoReturn")
    reject_id = fields.Many2one('reject.reason', string="Reject Reason")
    delivery_qty = fields.Float('Delivery QTY')
    return_qty = fields.Float('Return QTY')
    lot_ids = fields.Many2many('stock.lot', 'lot_rma_rel', 'lot_id', 'rma_id', string="Lot/Searial Number")
    price_before = fields.Float('Price Before')
    total = fields.Float('Total', compute="compute_total")
    sale_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")

    @api.depends('return_qty', 'price_before')
    def compute_total(self):
        for record in self:
            record.total = record.return_qty * record.price_before
