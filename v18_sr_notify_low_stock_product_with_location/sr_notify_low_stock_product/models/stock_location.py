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


class StockLocation(models.Model):
    _inherit = 'stock.location'

    min_qty = fields.Float(string="Min Qty")
    user_ids = fields.Many2many("res.users")
    min_qty_visible = fields.Boolean(compute="_compute_min_qty_visible")

    def _compute_min_qty_visible(self):
        for location in self:
            if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.apply_min_qty_on') == 'location':
                location.min_qty_visible = True
            else:
                location.min_qty_visible = False