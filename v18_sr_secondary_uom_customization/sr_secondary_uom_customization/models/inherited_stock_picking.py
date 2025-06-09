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


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_confirm(self):
        result = super(StockPicking, self).action_confirm()
        if self.move_ids_without_package:
            for move in self.move_ids_without_package:
                if move.move_line_ids:
                    for line in move.move_line_ids:
                        line.secondary_qty = line.move_id.secondary_qty
        return result

    def button_validate(self):
        if self.picking_type_id.code != 'incoming' and self.move_ids_without_package:
            quant_obj = self.env['stock.quant']

            for move in self.move_ids_without_package:
                for line in move.move_line_ids:
                    product = line.product_id
                    location = line.location_id
                    lot = line.lot_id
                    quantity_needed = line.quantity
                    secondary_qty_needed = line.secondary_qty

                    if not product or not location:
                        continue

                    domain = [('location_id', '=', location.id), ('product_id', '=', product.id)]
                    if lot:
                        domain.append(('lot_id', '=', lot.id))

                    quant_ids = quant_obj.search(domain)
                    total_quantity = sum(quant_ids.mapped('quantity'))

                    if total_quantity < quantity_needed:
                        if lot:
                            raise ValidationError(_(
                                '%(product_name)s :- Stock not available.',
                                product_name=lot.name
                            ))
                        else:
                            raise ValidationError(_(
                                '%(product_name)s :- Stock not available.',
                                product_name=product.display_name
                            ))

                    total_secondary_qty = sum(quant_ids.mapped('secondary_qty'))

                    if total_secondary_qty < secondary_qty_needed:
                        if lot:
                            raise ValidationError(_(
                                '%(product_name)s :- Secondary quantity stock not available.',
                                product_name=lot.name
                            ))
                        else:
                            raise ValidationError(_(
                                '%(product_name)s :- Secondary quantity stock not available.',
                                product_name=product.display_name
                            ))

        return super(StockPicking, self).button_validate()
