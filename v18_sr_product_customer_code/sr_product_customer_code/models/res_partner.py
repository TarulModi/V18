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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def show_product_code(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Product Codes',
            'res_model': 'product.customer.code',
            'view_mode': 'list',
            'domain': [('customer_id', '=', self.id)],
        }