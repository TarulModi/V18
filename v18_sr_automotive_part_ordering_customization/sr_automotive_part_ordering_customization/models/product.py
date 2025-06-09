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


class ProductVariant(models.Model):
    _inherit = 'product.product'

    default_code = fields.Char('Brand SKU Code', index=True)
    mrp = fields.Float('MRP')
    extra_variant_price = fields.Float('Extra Price')
    vehicle_ids = fields.Many2many('fleet.vehicle', 'product_vehicle_rel', 'product_id', 'vehicle_id', string='Models')
    brand_line_ids = fields.One2many('product.brand.line', 'product_id', string="Brand Line")
    model_code_ids = fields.One2many('product.model.code', 'product_id', string="Model code Data")
    product_variant_seller_ids = fields.One2many('product.supplierinfo', 'product_id')

    @api.depends('list_price', 'price_extra', 'extra_variant_price')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        super(ProductVariant, self)._compute_product_lst_price()
        for product in self:
            product.lst_price += product.extra_variant_price

    @api.onchange('lst_price')
    def _set_product_lst_price(self):
        for product in self:
            product.write({'list_price': product.list_price - product.extra_variant_price})

    # override base function
    def _price_compute(self, price_type, uom=None, currency=None, company=None, date=False):
        company = company or self.env.company
        date = date or fields.Date.context_today(self)

        self = self.with_company(company)
        if price_type == 'standard_price':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            self = self.sudo()

        prices = dict.fromkeys(self.ids, 0.0)
        for product in self:
            price = product[price_type] or 0.0
            price_currency = product.currency_id
            if price_type == 'standard_price':
                price_currency = product.cost_currency_id
            elif price_type == 'list_price':
                price += product._get_attributes_extra_price()
                # --------------START---------
                price += product.extra_variant_price
                # --------------STOP----------
            if uom:
                price = product.uom_id._compute_price(price, uom)

            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                price = price_currency._convert(price, currency, company, date)

            prices[product.id] = price

        return prices

    # override base function
    @api.depends("product_tmpl_id.write_date")
    def _compute_write_date(self):
        for record in self:
            record.write_date = max(record.write_date or self.env.cr.now(), record.product_tmpl_id.write_date or self.env.cr.now())
