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
from odoo import api, fields, models, _, Command, SUPERUSER_ID


class MRP(models.Model):
    _inherit = "mrp.production"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary', store=True)
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")

    @api.onchange('product_qty')
    def onchange_product_qty(self):
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.product_qty
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.product_qty
            print("------move_raw_ids--move_raw_ids---", self.move_raw_ids)

    @api.onchange('qty_producing', 'lot_producing_id')
    def _onchange_producing(self):
        result = super(MRP, self)._onchange_producing()
        print("----self.move_raw_ids---------", self.move_raw_ids)
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.qty_producing
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.qty_producing

        # if self.move_raw_ids:
        #     for move in self.move_raw_ids:
        #         if move and move.quantity > 0:
        #             move.onchange_quantity()
        #         else:
        #             move.onchange_product_uom_qty()
        return result

    @api.depends('company_id', 'bom_id', 'product_id', 'product_qty', 'product_uom_id', 'location_src_id',
                 'never_product_template_attribute_value_ids')
    def _compute_move_raw_ids(self):
        for production in self:
            if production.state != 'draft' or self.env.context.get('skip_compute_move_raw_ids'):
                continue
            list_move_raw = [Command.link(move.id) for move in
                             production.move_raw_ids.filtered(lambda m: not m.bom_line_id)]
            if not production.bom_id and not production._origin.product_id:
                production.move_raw_ids = list_move_raw
            if any(move.bom_line_id.bom_id != production.bom_id or move.bom_line_id._skip_bom_line(
                    production.product_id, production.never_product_template_attribute_value_ids)
                   for move in production.move_raw_ids if move.bom_line_id):
                production.move_raw_ids = [Command.clear()]
            if production.bom_id and production.product_id and production.product_qty > 0:
                # keep manual entries
                production.secondary_qty = production.bom_id.secondary_qty
                moves_raw_values = production._get_moves_raw_values()
                move_raw_dict = {move.bom_line_id.id: move for move in
                                 production.move_raw_ids.filtered(lambda m: m.bom_line_id)}
                for move_raw_values in moves_raw_values:
                    if move_raw_values['bom_line_id'] in move_raw_dict:
                        # update existing entries
                        list_move_raw += [
                            Command.update(move_raw_dict[move_raw_values['bom_line_id']].id, move_raw_values)]
                    else:
                        # add new entries
                        list_move_raw += [Command.create(move_raw_values)]
                production.move_raw_ids = list_move_raw
            else:
                production.move_raw_ids = [Command.delete(move.id) for move in
                                           production.move_raw_ids.filtered(lambda m: m.bom_line_id)]
                production.secondary_qty = 0.0

    def _get_move_raw_values(self, product, product_uom_qty, product_uom, operation_id=False, bom_line=False):
        """ Warning, any changes done to this method will need to be repeated for consistency in:
            - Manually added components, i.e. "default_" values in view
            - Moves from a copied MO, i.e. move.create
            - Existing moves during backorder creation """
        source_location = self.location_src_id
        data = {
            'sequence': bom_line.sequence if bom_line else 10,
            'name': _('New'),
            'date': self.date_start,
            'date_deadline': self.date_start,
            'bom_line_id': bom_line.id if bom_line else False,
            'picking_type_id': self.picking_type_id.id,
            'product_id': product.id,
            'product_uom_qty': product_uom_qty,
            'product_uom': product_uom.id,
            'location_id': source_location.id,
            'location_dest_id': self.product_id.with_company(self.company_id).property_stock_production.id,
            'raw_material_production_id': self.id,
            'company_id': self.company_id.id,
            'operation_id': operation_id,
            'procure_method': 'make_to_stock',
            'origin': self._get_origin(),
            'state': 'draft',
            'warehouse_id': source_location.warehouse_id.id,
            'group_id': self.procurement_group_id.id,
            'propagate_cancel': self.propagate_cancel,
            'manual_consumption': self.env['stock.move']._determine_is_manual_consumption(bom_line),
            'secondary_qty' : bom_line.secondary_qty,
        }
        print("------_get_move_raw_values---data----------",data)
        return data

    def action_confirm(self):
        result = super(MRP, self).action_confirm()
        if self.move_raw_ids and self.move_raw_ids.move_line_ids:
            for line in self.move_raw_ids.move_line_ids:
                line.secondary_qty = line.move_id.secondary_qty

        if self.finished_move_line_ids:
            for line in self.finished_move_line_ids:
                line.secondary_qty = line.move_id.production_id.secondary_qty
        return result

    def button_mark_done(self):
        if self.move_raw_ids:
            quant_obj = self.env['stock.quant']

            for move in self.move_raw_ids:
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

        return super(MRP, self).button_mark_done()

    # @api.onchange('product_qty')
    # def _onchange_product_qty_secondary_qty(self):
    #     for production in self:
    #         if production.move_raw_ids:
    #             print('--Move Raw--', production)
    #             qty_diff = production.product_qty - (production._origin.product_qty or 0.0)
    #             print('---MOVE IDs---', qty_diff)
    #             if qty_diff != 0:
    #                 for move in production.move_raw_ids:
    #                     if move.secondary_qty is not None:
    #                         move.secondary_qty += qty_diff
