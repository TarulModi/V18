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


class SrPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    diff_ship = fields.Boolean(string="Separate shipment per line")

    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        if not self.diff_ship:
            return super()._create_picking()
        else:
            for line in self.order_line:
                if line.product_id.type in ['product', 'consu']:
                    picking_vals = self._prepare_picking()
                    picking = StockPicking.create(picking_vals)
                    moves = line._create_stock_moves(picking)
                    moves = moves.filtered(lambda m: m.state not in ('done', 'cancel'))._action_confirm()
                    seq = 0
                    for move in sorted(moves, key=lambda m: m.date):
                        seq += 5
                        move.sequence = seq
                    moves._action_assign()

                    picking.message_post(
                        body="Shipment created from purchase order <b>%s</b>" % self.name,
                        subtype_id=self.env.ref('mail.mt_note').id,
                    )
        return True



