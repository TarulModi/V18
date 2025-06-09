# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields


class stock_move(models.Model):
    _inherit = 'stock.move'

    created_sale_order_line_id = fields.Many2one('sale.order.line', string="Order Line")
