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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_code_ids = fields.One2many('product.customer.code' , 'product_template_id')
    x_customer_code_search = fields.Char(string='Customer Code', compute='compute_code',search='search_customer_code', store=False)

    def compute_code(self):
        for rec in self:
            rec.x_customer_code_search = ''

    def search_customer_code(self, operator, value):
        if not value:
            return []
        product_codes = self.env['product.customer.code'].search([('code', operator, value)])
        template_ids = product_codes.mapped('product_template_id').ids
        return [('id', 'in', template_ids)]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        try:
            if args is None:
                args = []

            partner_id = self._context.get('default_partner_id') or \
                         self._context.get('partner_id') or \
                         self._context.get('parent_partner_id')

            if partner_id and name and name.strip():
                exact_codes = self.env['product.customer.code'].search([
                    ('customer_id', '=', partner_id),
                    ('code', '=', name.strip())
                ], limit=limit)

                if exact_codes:
                    templates = exact_codes.mapped('product_template_id')
                    return [(t.id, f"{t.name} [{t.default_code or ''}]") for t in templates]

                partial_codes = self.env['product.customer.code'].search([
                    ('customer_id', '=', partner_id),
                    ('code', 'ilike', name.strip())
                ], limit=limit)

                if partial_codes:
                    templates = partial_codes.mapped('product_template_id')
                    return [(t.id, f"{t.name} [{t.default_code or ''}]") for t in templates]

            return super().name_search(name, args, operator, limit)

        except Exception:
            return super().name_search(name, args, operator, limit)