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


class ProductCustomerCode(models.Model):
    _name = 'product.customer.code'
    _description = 'Product Customer Code'

    customer_id = fields.Many2one('res.partner', string='Customer')
    code = fields.Char(string='Customer Product Code')
    name = fields.Char(string='Customer Product Name')
    product_template_id = fields.Many2one('product.template', string='Product')
    product_variant_id = fields.Many2one('product.product',string='Product Variant',domain="[('product_tmpl_id', '=', product_template_id)] if product_template_id else []")

    apply_to_all_variants = fields.Boolean(compute='_compute_apply_to_all_variants', store=True)


    _sql_constraints = [
        # This works only when no NULLs are present
        (
            'unique_customer_template_variant_code',
            'UNIQUE(customer_id, product_template_id, product_variant_id, code)',
            'Duplicate: same customer/product/code combination already exists.'
        ),
    ]

    @api.constrains('customer_id', 'product_template_id', 'product_variant_id', 'code')
    def _check_combinations(self):
        for record in self:
            domain_base = [('id', '!=', record.id)] if record.id else []

            # 1. customer_id + product_variant_id
            if record.customer_id and record.product_variant_id:
                if self.search_count([
                                         ('customer_id', '=', record.customer_id.id),
                                         ('product_variant_id', '=', record.product_variant_id.id),
                                     ] + domain_base):
                    raise ValidationError(
                        _('Duplicate: This customer already has an entry for this product variant.')
                    )

            # 2. customer_id + product_template_id + product_variant_id
            if record.customer_id and record.product_template_id and record.product_variant_id:
                if self.search_count([
                                         ('customer_id', '=', record.customer_id.id),
                                         ('product_template_id', '=', record.product_template_id.id),
                                         ('product_variant_id', '=', record.product_variant_id.id),
                                     ] + domain_base):
                    raise ValidationError(
                        _('Duplicate: This customer already has this product template + variant combination.')
                    )

            # 3. customer_id + product_variant_id + code
            if record.customer_id and record.product_variant_id and record.code:
                if self.search_count([
                                         ('customer_id', '=', record.customer_id.id),
                                         ('product_variant_id', '=', record.product_variant_id.id),
                                         ('code', '=', record.code),
                                     ] + domain_base):
                    raise ValidationError(
                        _('Duplicate: This customer already has this code for this product variant.')
                    )

            # 4. customer_id + product_template_id (when product_variant_id is null)
            if record.customer_id and record.product_template_id and not record.product_variant_id:
                if self.search_count([
                                         ('customer_id', '=', record.customer_id.id),
                                         ('product_template_id', '=', record.product_template_id.id),
                                         ('product_variant_id', '=', False),
                                     ] + domain_base):
                    raise ValidationError(
                        _('Duplicate: This customer already has a template-level entry for this product.')
                    )

    @api.depends('product_variant_id')
    def _compute_apply_to_all_variants(self):
        for record in self:
            record.apply_to_all_variants = not bool(record.product_variant_id)

    @api.model_create_multi
    def create(self, vals_list):
        records = []

        for vals in vals_list:
            # Auto-set product_template_id if product_variant_id is given and template not set
            if vals.get('product_variant_id') and not vals.get('product_template_id'):
                product = self.env['product.product'].browse(vals['product_variant_id'])
                vals['product_template_id'] = product.product_tmpl_id.id

            # If it's a template-level entry (no variant), create per-variant lines and skip this one
            if vals.get('product_template_id') and not vals.get('product_variant_id'):
                template = self.env['product.template'].browse(vals['product_template_id'])
                for variant in template.product_variant_ids:
                    record_vals = vals.copy()
                    record_vals['product_variant_id'] = variant.id
                    records.append(super().create(record_vals))
            else:
                records.append(super().create(vals))

        return self.browse([r.id for r in records])

    def write(self, vals):
        if vals.get('product_variant_id') and not vals.get('product_template_id'):
            product = self.env['product.product'].browse(vals['product_variant_id'])
            vals['product_template_id'] = product.product_tmpl_id.id
        res = super().write(vals)

        if any(field in vals for field in ['code', 'name']):
            for record in self.filtered(lambda r: r.product_template_id and not r.product_variant_id):
                record._apply_code_to_all_variants()
        return res

    def _apply_code_to_all_variants(self):
        self.ensure_one()

        if self.product_variant_id or not self.product_template_id:
            return

        variants = self.product_template_id.product_variant_ids
        existing = self.search_read([
            ('customer_id', '=', self.customer_id.id),
            ('product_template_id', '=', self.product_template_id.id),
            ('product_variant_id', 'in', variants.ids),
        ], ['id', 'product_variant_id'])

        existing_map = {rec['product_variant_id'][0]: rec['id'] for rec in existing}

        records_to_write = []
        records_to_create = []

        for variant in variants:
            if variant.id in existing_map:
                records_to_write.append((existing_map[variant.id], {
                    'code': self.code,
                    'name': self.name
                }))
            else:
                records_to_create.append({
                    'customer_id': self.customer_id.id,
                    'code': self.code,
                    'name': self.name,
                    'product_template_id': self.product_template_id.id,
                    'product_variant_id': variant.id,
                })

        for rec_id, vals in records_to_write:
            self.browse(rec_id).write(vals)

        if records_to_create:
            self.env['product.customer.code'].create(records_to_create)

    @api.onchange('product_template_id')
    def _onchange_product_template_id(self):
        if self.product_variant_id and self.product_variant_id.product_tmpl_id != self.product_template_id:
            self.product_variant_id = False

    @api.onchange('product_variant_id')
    def _onchange_product_variant_id(self):
        if self.product_variant_id:
            self.product_template_id = self.product_variant_id.product_tmpl_id
