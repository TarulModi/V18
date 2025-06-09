# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from email.policy import default

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    secondary_qty = fields.Float("Secondary Quantity", tracking=True, digits='Secondary')
    secondary_uom_id = fields.Many2one(related="product_id.secondary_uom_id")
    is_secondary = fields.Boolean(related="product_id.is_secondary")

    _sql_constraints = [
        ('check_secondary_qty_positive',
         'CHECK(secondary_qty >= 0)',
         'Secondary quantity must be a non-negative value.')
    ]

    @api.onchange('quantity', 'product_uom_id')
    def _onchange_quantity(self):
        result = super(StockMoveLine, self)._onchange_quantity()
        if self.product_id and self.product_id.is_secondary:
            if self.product_id.dynamic_ratio > 0:
                self.secondary_qty = self.product_id.dynamic_ratio * self.quantity
            else:
                self.secondary_qty = self.product_id.standard_ratio * self.quantity
        return result

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('move_id'):
                vals['company_id'] = self.env['stock.move'].browse(vals['move_id']).company_id.id
                # #======================= custom code ===================
                move_id = self.env['stock.move'].browse(vals['move_id'])
                if move_id and move_id.product_id and move_id.product_id.is_secondary:
                    if move_id.raw_material_production_id and not move_id.raw_material_production_id.move_raw_line_ids:
                        vals['secondary_qty'] = move_id.secondary_qty
                    else:
                        if move_id.raw_material_production_id and move_id.raw_material_production_id.move_raw_line_ids:
                            line_ids = move_id.raw_material_production_id.move_raw_line_ids.filtered(
                                lambda r: r.product_id.id == vals['product_id']
                            )
                            if line_ids:
                                continue
                            else:
                                vals['secondary_qty'] = move_id.secondary_qty
                # #====================end============================
            elif vals.get('picking_id'):
                vals['company_id'] = self.env['stock.picking'].browse(vals['picking_id']).company_id.id
            if vals.get('move_id') and 'picked' not in vals:
                vals['picked'] = self.env['stock.move'].browse(vals['move_id']).picked
            if vals.get('quant_id'):
                vals.update(self._copy_quant_info(vals))

        mls = super().create(vals_list)

        def create_move(move_line):
            new_move = self.env['stock.move'].create(move_line._prepare_stock_move_vals())
            move_line.move_id = new_move.id

        # If the move line is directly create on the picking view.
        # If this picking is already done we should generate an
        # associated done move.
        for move_line in mls:
            if move_line.move_id or not move_line.picking_id:
                continue
            if move_line.picking_id.state != 'done':
                moves = move_line._get_linkable_moves()
                if moves:
                    vals = {
                        'move_id': moves[0].id,
                        'picking_id': moves[0].picking_id.id,
                    }
                    if moves[0].picked:
                        vals['picked'] = True
                    move_line.write(vals)
                else:
                    create_move(move_line)
            else:
                create_move(move_line)

        move_to_recompute_state = set()
        for move_line in mls:
            if move_line.secondary_qty == 0 and move_line.product_id and move_line.product_id.is_secondary:
                move_line.secondary_qty = move_line.move_id.secondary_qty
            if move_line.state == 'done':
                continue
            location = move_line.location_id
            product = move_line.product_id
            move = move_line.move_id
            if move:
                reservation = not move._should_bypass_reservation()
            else:
                reservation = product.is_storable and not location.should_bypass_reservation()
            if move_line.quantity and reservation:
                self.env.context.get('reserved_quant', self.env['stock.quant'])._update_reserved_quantity(
                    product, location, move_line.quantity_product_uom, lot_id=move_line.lot_id,
                    package_id=move_line.package_id, owner_id=move_line.owner_id)

                if move:
                    move_to_recompute_state.add(move.id)
        self.env['stock.move'].browse(move_to_recompute_state)._recompute_state()

        for ml, vals in zip(mls, vals_list):
            if ml.state == 'done':
                if ml.product_id.is_storable:
                    Quant = self.env['stock.quant']
                    quantity = ml.product_uom_id._compute_quantity(ml.quantity, ml.move_id.product_id.uom_id,
                                                                   rounding_method='HALF-UP')
                    in_date = None
                    available_qty, in_date = Quant._update_available_quantity(ml.product_id, ml.location_id, -quantity,
                                                                              lot_id=ml.lot_id,
                                                                              package_id=ml.package_id,
                                                                              owner_id=ml.owner_id)
                    if available_qty < 0 and ml.lot_id:
                        # see if we can compensate the negative quants with some untracked quants
                        untracked_qty = Quant._get_available_quantity(ml.product_id, ml.location_id, lot_id=False,
                                                                      package_id=ml.package_id, owner_id=ml.owner_id,
                                                                      strict=True)
                        if untracked_qty:
                            taken_from_untracked_qty = min(untracked_qty, abs(quantity))
                            Quant._update_available_quantity(ml.product_id, ml.location_id, -taken_from_untracked_qty,
                                                             lot_id=False, package_id=ml.package_id,
                                                             owner_id=ml.owner_id)
                            Quant._update_available_quantity(ml.product_id, ml.location_id, taken_from_untracked_qty,
                                                             lot_id=ml.lot_id, package_id=ml.package_id,
                                                             owner_id=ml.owner_id)
                    Quant._update_available_quantity(ml.product_id, ml.location_dest_id, quantity, lot_id=ml.lot_id,
                                                     package_id=ml.result_package_id, owner_id=ml.owner_id,
                                                     in_date=in_date)
                next_moves = ml.move_id.move_dest_ids.filtered(lambda move: move.state not in ('done', 'cancel'))
                next_moves._do_unreserve()
                next_moves._action_assign()
        move_done = mls.filtered(lambda m: m.state == "done").move_id
        if move_done:
            move_done._check_quantity()
        return mls

    def _synchronize_quant(self, quantity, location, action="available", in_date=False, **quants_value):
        """ quantity should be express in product's UoM"""
        lot = quants_value.get('lot', self.lot_id)
        package = quants_value.get('package', self.package_id)
        owner = quants_value.get('owner', self.owner_id)
        available_qty = 0
        if not self.product_id.is_storable or float_is_zero(quantity, precision_rounding=self.product_uom_id.rounding):
            return 0, False
        if action == "available":
            if self.secondary_qty:
                if quantity < 0:
                    secondary_qty = - (self.secondary_qty)
                else:
                    secondary_qty = self.secondary_qty
                available_qty, in_date = self.env['stock.quant'].with_context(secondary_qty=secondary_qty)._update_available_quantity(self.product_id, location,
                                                                                            quantity, lot_id=lot,
                                                                                            package_id=package,
                                                                                            owner_id=owner,
                                                                                            in_date=in_date)
            else:
                available_qty, in_date = self.env['stock.quant']._update_available_quantity(self.product_id, location,
                                                                                        quantity, lot_id=lot,
                                                                                        package_id=package,
                                                                                        owner_id=owner, in_date=in_date)
        elif action == "reserved" and not self.move_id._should_bypass_reservation(location):
            if self.secondary_qty:
                if quantity < 0:
                    secondary_qty = - (self.secondary_qty)
                else:
                    secondary_qty = self.secondary_qty
                self.env['stock.quant'].with_context(secondary_qty=secondary_qty)._update_reserved_quantity(self.product_id, location, quantity, lot_id=lot,
                                                                  package_id=package, owner_id=owner)
            else:
                self.env['stock.quant']._update_reserved_quantity(self.product_id, location, quantity, lot_id=lot,
                                                              package_id=package, owner_id=owner)
        if available_qty < 0 and lot:
            # see if we can compensate the negative quants with some untracked quants
            untracked_qty = self.env['stock.quant']._get_available_quantity(self.product_id, location, lot_id=False,
                                                                            package_id=package, owner_id=owner,
                                                                            strict=True)
            if not untracked_qty:
                return available_qty, in_date
            taken_from_untracked_qty = min(untracked_qty, abs(quantity))
            self.env['stock.quant']._update_available_quantity(self.product_id, location, -taken_from_untracked_qty,
                                                               lot_id=False, package_id=package, owner_id=owner,
                                                               in_date=in_date)
            self.env['stock.quant']._update_available_quantity(self.product_id, location, taken_from_untracked_qty,
                                                               lot_id=lot, package_id=package, owner_id=owner,
                                                               in_date=in_date)
        return available_qty, in_date
