# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    so_id = fields.Many2one("sale.order",string='Sale Order')
    can_confirm_po = fields.Boolean("Can confirm PO?", default=False, compute='_compute_can_confirm_po')

    def _compute_can_confirm_po(self):
        user_ids = self.env.company.insufficient_stock_email_user_ids
        if self.env.user.id in user_ids.ids:
            self.can_confirm_po = True
        else:
            self.can_confirm_po = False


    @api.onchange('so_id')
    def _onchange_so_id(self):
        if not self.so_id:
            return

        order_lines_data = [fields.Command.clear()]
        order_lines_data += [
            fields.Command.create(line._prepare_order_line_values())
            for line in self.so_id.order_line if line.prod_type == 'non_stockable'
        ]
        self.order_line = order_lines_data
