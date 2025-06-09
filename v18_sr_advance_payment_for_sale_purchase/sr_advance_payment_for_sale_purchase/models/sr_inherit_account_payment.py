# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, _


class srAccountPayment(models.Model):
    _inherit = "account.payment"

    sale_order_id = fields.Many2one('sale.order', string="Sales Order", copy=False)
    purchase_order_id = fields.Many2one('purchase.order', string="Purchase Order", copy=False)
