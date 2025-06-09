# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from collections import defaultdict
from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary', store=True)
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")

    _sql_constraints = [
        ('check_secondary_qty_positive',
         'CHECK(secondary_qty >= 0)',
         'Secondary quantity must be a non-negative value.')
    ]

    @api.onchange('product_uom_qty')
    def onchange_product_uom_qty(self):
        print("-------11--------11-------", self.production_id)
        print("----22----------111--------", self.raw_material_production_id)
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.product_uom_qty
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.product_uom_qty

    @api.depends('move_line_ids.quantity', 'move_line_ids.product_uom_id', 'move_line_ids.secondary_qty')
    def _compute_quantity(self):
        """ This field represents the sum of the move lines `quantity`. It allows the user to know
        if there is still work to do.

        We take care of rounding this value at the general decimal precision and not the rounding
        of the move's UOM to make sure this value is really close to the real sum, because this
        field will be used in `_action_done` in order to know if the move will need a backorder or
        an extra move.
        """
        if not any(self._ids):
            # onchange
            for move in self:
                move.quantity = move._quantity_sml()
                if move.product_id and move.product_id.is_secondary:
                    sum_move_line = sum(move.move_line_ids.mapped('secondary_qty'))
                    move.secondary_qty = sum_move_line
        else:
            # compute
            move_lines_ids = set()
            for move in self:
                move_lines_ids |= set(move.move_line_ids.ids)

            data = self.env['stock.move.line']._read_group(
                [('id', 'in', list(move_lines_ids))],
                ['move_id', 'product_uom_id'], ['quantity:sum']
            )
            sum_qty = defaultdict(float)
            for move, product_uom, qty_sum in data:
                uom = move.product_uom
                sum_qty[move.id] += product_uom._compute_quantity(qty_sum, uom, round=False)

            for move in self:
                move.quantity = sum_qty[move.id]

    def write(self, vals):
        result = super(StockMove, self).write(vals)
        for record in self:
            if record.move_line_ids and record.product_id and record.product_id.is_secondary:
                if 'secondary_qty' in vals and vals['secondary_qty'] and not 'move_line_ids' in vals:
                    for line in record.move_line_ids:
                        if line.move_id.secondary_qty and line.move_id.quantity:
                            line.secondary_qty = line.move_id.secondary_qty

                if 'quantity' in vals and not 'secondary_qty' in vals:
                    if record.product_id.dynamic_ratio > 0:
                        record.secondary_qty = record.product_id.dynamic_ratio * record.quantity
                    else:
                        record.secondary_qty = record.product_id.standard_ratio * record.quantity
        return result
