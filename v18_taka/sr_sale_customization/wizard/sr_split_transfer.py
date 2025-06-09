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
from odoo.exceptions import UserError, ValidationError


class SplitTransfer(models.TransientModel):
    _name = 'sr.split.transfer'
    _description = 'Split Transfer'

    picking_move_line_ids = fields.One2many("sr.split.move.line", 'split_wizard_id', "Move Lines")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        if self.env.context.get('active_id'):
            picking_id = self.env['stock.picking'].browse([self.env.context.get('active_id')]).exists()
            if picking_id and picking_id.move_ids_without_package:
                move_lst = []
                for line in picking_id.move_ids_without_package:
                    move_lst.append((0, 0, {
                        'product_id' : line.product_id.id,
                        'demand_qty' : line.product_uom_qty,
                        'quantity': line.quantity,
                        'move_id' : line.id
                    }))
                defaults['picking_move_line_ids'] = move_lst
        return defaults

    def split_transfer(self):
        split_moves = self.picking_move_line_ids.filtered(lambda l: l.is_split).move_id
        if len(split_moves) == len(self.picking_move_line_ids):
            raise ValidationError(_('You can not split transfer with all items'))
        if self.env.context.get('active_id'):
            picking_id = self.env['stock.picking'].browse([self.env.context.get('active_id')]).exists()
            if picking_id:
                picking_id._create_backorder(backorder_moves=split_moves)


class SplitMoveLine(models.TransientModel):
    _name = 'sr.split.move.line'
    _description = 'Split Move Line'

    split_wizard_id = fields.Many2one('sr.split.transfer')
    move_id = fields.Many2one("stock.move", string="Stock Move")
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float("Quantity")
    demand_qty = fields.Float("Demand")
    is_split = fields.Boolean("Split?")
