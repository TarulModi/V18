# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        if self.order_line:
            for line in self.order_line:
                if line.qty_available_today < line.product_uom_qty:
                    raise ValidationError(_(
                        '%(product_name)s :- Stock not available.',
                        product_name=line.product_id.display_name
                    ))
        result = super(SaleOrder, self).action_confirm()
        if self.picking_ids:
            for picking in self.picking_ids:
                if picking.move_ids_without_package:
                    for move in picking.move_ids_without_package:
                        move.secondary_qty = move.sale_line_id.secondary_qty
                        if move.move_line_ids:
                            for line in move.move_line_ids:
                                line.secondary_qty = line.move_id.secondary_qty
        return result
