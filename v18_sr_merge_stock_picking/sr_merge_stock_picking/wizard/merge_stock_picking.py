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
from odoo.exceptions import ValidationError


class MergePicking(models.TransientModel):
    _name = 'merge.picking'
    _description = 'Merge Stock Pickings (Receipts)'

    merge_type = fields.Selection(selection=[
        ("new_cancel_selected",         "New Picking and Cancel Selected"),
        ("new_delete_all_selected",     "New Picking and Delete Selected"),
        ("merge_selected_cancel_other", "Merge Into Existing and Cancel Others"),
        ("merge_selected_delete_other", "Merge Into Existing and Delete Others"),
    ], default="new_cancel_selected", required=True, string="Merge Type")

    merge_with = fields.Many2one(
        'stock.picking',
        string="Merge With",
        domain="[('id', 'in', context.get('active_ids', []))]",
        help="Select the picking to merge with when merging into an existing picking."
    )

    @api.onchange('merge_type')
    def _onchange_merge_type(self):
        if self.merge_type not in ["merge_selected_cancel_other", "merge_selected_delete_other"]:
            self.merge_with = False

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self._context.get('active_ids', [])

        if not active_ids:
            raise ValidationError(_("Please select at least one picking."))
        if len(active_ids) < 2:
            raise ValidationError(_("Please select multiple pickings to merge in the list view."))

        pickings = self.env['stock.picking'].browse(active_ids)
        partners = {p.partner_id.id for p in pickings if p.partner_id}
        picking_types = {p.picking_type_id.code for p in pickings if p.picking_type_id}

        if any(p.state in ('done', 'cancel') for p in pickings):
            raise ValidationError(_("Cannot merge pickings that are already Done or Cancelled."))
        if any(not p.partner_id for p in pickings) and partners:
            raise ValidationError(_("All selected pickings must have the same partner or none."))
        if len(partners) > 1:
            raise ValidationError(_("All selected pickings must have the same partner."))
        if len(picking_types) > 1:
            raise ValidationError(_("All selected pickings must have the same Operation Type."))

        return res

    def action_merge_pickings(self):
        pickings = self.env['stock.picking'].browse(self._context.get('active_ids', []))

        def merge_lines(source_lines, target_picking):
            for line in source_lines:
                existing = target_picking.move_ids_without_package.filtered(
                    lambda l: l.product_id == line.product_id and
                              l.product_uom == line.product_uom and
                              l.location_id == line.location_id and
                              l.location_dest_id == line.location_dest_id
                )
                if existing:
                    existing.quantity += line.quantity
                else:
                    line.copy(default={"picking_id": target_picking.id})

        if self.merge_type in ['new_cancel_selected', 'new_delete_all_selected']:
            picking_type = pickings[0].picking_type_id
            partner = pickings[0].partner_id
            origin = ', '.join(filter(None, pickings.mapped('origin')))

            new_picking = self.env['stock.picking'].create({
                'picking_type_id': picking_type.id,
                'partner_id': partner.id,
                'location_id': pickings[0].location_id.id,
                'location_dest_id': pickings[0].location_dest_id.id,
                'origin': origin,
            })

            for picking in pickings:
                merge_lines(picking.move_ids_without_package, new_picking)

            for picking in pickings:
                picking.action_cancel()
                if self.merge_type == "new_delete_all_selected":
                    picking.sudo().unlink()

        elif self.merge_type in ['merge_selected_cancel_other', 'merge_selected_delete_other']:
            target = self.merge_with or pickings[0]

            for picking in pickings:
                if picking != target:
                    merge_lines(picking.move_ids_without_package, target)

            for picking in pickings:
                if picking != target:
                    picking.action_cancel()
                    if self.merge_type == 'merge_selected_delete_other':
                        picking.sudo().unlink()
