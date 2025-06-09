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


class rmaReplacedProduct(models.Model):
    _name = 'rma.replaced.product'
    _description = 'RMA Replaced Product'
    _rec_name = 'product_id'
    _inherit = ['mail.thread']

    rma_order_id = fields.Many2one("rma.order")
    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Float('Quantity')
    price = fields.Float('Price')
    total = fields.Float('Total Price', compute="compute_total")

    @api.depends('qty', 'price')
    def compute_total(self):
        for record in self:
            record.total = record.qty * record.price
