# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.exceptions import UserError
from odoo import _, api, fields, models, tools
from odoo.tools import float_is_zero, check_barcode_encoding


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'secondary_uom_id' in fields_list and not res.get('secondary_uom_id'):
            res['secondary_uom_id'] = self._get_default_secondary_uom_id().id
        return res

    @tools.ormcache()
    def _get_default_secondary_uom_id(self):
        # Deletion forbidden (at least through unlink)
        return self.env.ref('uom.product_uom_unit')

    secondary_uom_id = fields.Many2one(
        'uom.uom', 'Secondary UOM',
        default=_get_default_secondary_uom_id, required=True, tracking=True)

    standard_ratio = fields.Float("Standard Ratio", default="1", tracking=True, digits='Secondary', copy=False)
    dynamic_ratio = fields.Float("Dynamic Ratio", default="1", tracking=True, compute="calculate_dynamic_ratio", digits='Secondary', copy=False)
    is_secondary = fields.Boolean("Is Secondary", tracking=True)

    _sql_constraints = [
        ('check_standard_ratio_positive',
         'CHECK(standard_ratio >= 0)',
         'Standard Ratio must be a non-negative value.')
    ]

    @api.depends('qty_available')
    def calculate_dynamic_ratio(self):
        for record in self:
            quant_ids = self.env['stock.quant'].search([
                ('product_tmpl_id', '=', record.id),
                ('location_id.usage', 'in', ['internal', 'transit'])
            ])
            if quant_ids:
                secondary_qty = sum(quant_ids.mapped('secondary_qty'))
                quantity = sum(quant_ids.mapped('quantity'))
                record.dynamic_ratio = (secondary_qty / quantity) if quantity != 0 else 0.0
            else:
                record.dynamic_ratio = 0.0

    def write(self, vals):
        if 'company_id' in vals and vals['company_id']:
            products_changing_company = self.filtered(lambda product: product.company_id.id != vals['company_id'])
            if products_changing_company:
                move = self.env['stock.move'].sudo().search([
                    ('product_id', 'in', products_changing_company.product_variant_ids.ids),
                    ('company_id', 'not in', [vals['company_id'], False]),
                ], order=None, limit=1)
                if move:
                    raise UserError(
                        _("This product's company cannot be changed as long as there are stock moves of it belonging to another company."))

                # Forbid changing a product's company when quant(s) exist in another company.
                quant = self.env['stock.quant'].sudo().search([
                    ('product_id', 'in', products_changing_company.product_variant_ids.ids),
                    ('company_id', 'not in', [vals['company_id'], False]),
                    ('quantity', '!=', 0),
                ], order=None, limit=1)
                if quant:
                    raise UserError(
                        _("This product's company cannot be changed as long as there are quantities of it belonging to another company."))

        if 'uom_id' in vals:
            new_uom = self.env['uom.uom'].browse(vals['uom_id'])
            updated = self.filtered(lambda template: template.uom_id != new_uom)
            done_moves = self.env['stock.move'].sudo().search(
                [('product_id', 'in', updated.with_context(active_test=False).mapped('product_variant_ids').ids)],
                limit=1)
            if done_moves:
                raise UserError(
                    _("You cannot change the unit of measure as there are already stock moves for this product. If you want to change the unit of measure, you should rather archive this product and create a new one."))

        #-------------------------start-------------------------------------
        if 'secondary_uom_id' in vals:
            new_uom = self.env['uom.uom'].browse(vals['secondary_uom_id'])
            updated = self.filtered(lambda template: template.uom_id != new_uom)
            done_moves = self.env['stock.move'].sudo().search(
                [('product_id', 'in', updated.with_context(active_test=False).mapped('product_variant_ids').ids)],
                limit=1)
            if done_moves:
                raise UserError(
                    _("You cannot change the unit of measure as there are already stock moves for this product. If you want to change the unit of measure, you should rather archive this product and create a new one."))
        #----------------------------end----------------------------------
        if 'is_storable' in vals and not vals['is_storable'] and sum(self.mapped('nbr_reordering_rules')) != 0:
            raise UserError(
                _('You still have some active reordering rules on this product. Please archive or delete them first.'))
        if any('is_storable' in vals and vals['is_storable'] != prod_tmpl.is_storable for prod_tmpl in self):
            existing_done_move_lines = self.env['stock.move.line'].sudo().search([
                ('product_id', 'in', self.with_context(active_test=False).mapped('product_variant_ids').ids),
                ('state', '=', 'done'),
            ], limit=1)
            if existing_done_move_lines:
                raise UserError(_("You can not change the inventory tracking of a product that was already used."))
            existing_reserved_move_lines = self.env['stock.move.line'].sudo().search([
                ('product_id', 'in', self.with_context(active_test=False).mapped('product_variant_ids').ids),
                ('state', 'in', ['partially_available', 'assigned']),
            ], limit=1)
            if existing_reserved_move_lines:
                raise UserError(
                    _("You can not change the inventory tracking of a product that is currently reserved on a stock move. If you need to change the inventory tracking, you should first unreserve the stock move."))
        if 'is_storable' in vals and not vals['is_storable'] and any(
                p.is_storable and not float_is_zero(p.qty_available, precision_rounding=p.uom_id.rounding) for p in
                self):
            raise UserError(_("Available quantity should be set to zero before changing inventory tracking"))
        return super().write(vals)
