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
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    is_picking_type_split_transfer = fields.Boolean(string='Picking Type Split Transfer?', compute="_compute_picking_type_split_type")

    @api.depends('picking_type_id')
    def _compute_picking_type_split_type(self):
        for picking in self:
            if picking.picking_type_id and \
                picking.picking_type_id.warehouse_id.delivery_steps == 'pick_pack_ship' and \
                picking.picking_type_id.warehouse_id.pick_type_id == picking.picking_type_id:
                picking.is_picking_type_split_transfer = True
            else:
                picking.is_picking_type_split_transfer = False

    def action_split_picking_transfer(self):
        if len(self.move_ids_without_package.ids) <= 1:
            raise UserError(_('There is not enough items to split the transfer'))
        return {
            'name': _("Split The Transfer?"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'sr.split.transfer',
            'target': 'new',
        }
