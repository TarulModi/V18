# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    restrict_product_stock_in_sale_setting = fields.Boolean(
        string="Restrict Sales Quotation if Product is not in Stock", default=False,
        config_parameter='restrict_product_stock_in_sale_setting')

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sr_restrict_out_of_stock_sales_quotation.restrict_product_stock_in_sale_setting', self.restrict_product_stock_in_sale_setting)
        super(ResConfigSettings, self).set_values()

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        restrict_product_stock_in_sale_setting = ICPSudo.get_param('restrict_product_stock_in_sale_setting')
        res.update(
            restrict_product_stock_in_sale_setting=restrict_product_stock_in_sale_setting,
        )
        return res
