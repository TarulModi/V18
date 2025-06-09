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


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_code = fields.Char(
        'Brand SKU Code', compute='_compute_default_code',
        inverse='_set_default_code', store=True)
    amicco_sku_code = fields.Char('Amicco SKU Code')
    map_number = fields.Integer('Map Number')
    product_group_ids = fields.Many2many('product.template', 'product_tmpl_group_rel',
                                         'product_tmpl_id', 'group_id', string='Product Groups')
    product_tmpl_model_code_ids = fields.One2many('product.model.code', 'product_tmpl_id', string="Model code Data")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ProductTemplate, self).create(vals_list)
        for rec in res:
            code = ''
            if rec.name:
                split_name = rec.name.split('-')
                count = 0
                for word in split_name:
                    word = word.replace(' ', '')
                    count += 1
                    if count <= 3:
                        if count != 1:
                            code += '-'
                        code += word[:3] or word
                    else:
                        break
                char_count = code.count('-')
                if char_count <= 2:
                    for i in range(char_count, 2):
                        code += '-NA'
                code += '-' + str(rec.id)
            rec.amicco_sku_code = code
        return res

    def write(self, values):
        code = ''
        if values.get('name'):
            split_name = values.get('name').split('-')
            count = 0
            for word in split_name:
                word = word.replace(' ', '')
                count += 1
                if count <= 3:
                    if count != 1:
                        code += '-'
                    code += word[:3] or word
                else:
                    break
            char_count = code.count('-')
            if char_count <= 2:
                for i in range(char_count, 2):
                    code += '-NA'
            code += '-' + str(self.id)
            values['amicco_sku_code'] = code
        res = super(ProductTemplate, self).write(values)
        return res
