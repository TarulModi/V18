# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import ast
import json
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outgoing_mail_id = fields.Many2one("ir.mail_server")
    apply_min_qty_on = fields.Selection(
        [('global', 'Global'), ('product', 'Individual Product'), ('category', 'Product Category'),
         ('reorder_rule', 'Reorder Rule')])
    min_qty = fields.Float("Min Qty",default=0.0)
    notify_to = fields.Selection([('users', 'Users'), ('groups', 'Groups')])
    min_qty_user_ids = fields.Many2many("res.users", default=False)
    min_qty_group_ids = fields.Many2many("res.groups", default=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_user_ids'):
            user_ids_str = self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_user_ids')
            if user_ids_str:
                list_values = ast.literal_eval(user_ids_str)
                if list_values:
                    res['min_qty_user_ids'] = [(6, 0, list_values)]
                else:
                    res['min_qty_user_ids'] = [(6, 0, [])]
            else:
                res['min_qty_user_ids'] = [(6, 0, [])]
        else:
            res['min_qty_user_ids'] = [(6, 0, [])]     

        if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_group_ids'):
            group_ids_str = self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty_group_ids')
            if group_ids_str:
                list_values = ast.literal_eval(group_ids_str)
                if list_values:
                    res['min_qty_group_ids'] = [(6, 0, list_values)]
                else:
                    res['min_qty_group_ids'] = [(6, 0, [])]
            else:
                res['min_qty_group_ids'] = [(6, 0, [])]
        else:
            res['min_qty_group_ids'] = [(6, 0, [])]

        if self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.outgoing_mail_id'):
            res['outgoing_mail_id'] = int(self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.outgoing_mail_id', default=0))
        res['apply_min_qty_on'] = self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.apply_min_qty_on')
        res['min_qty'] = float(self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.min_qty', default= 0.0))
        res['notify_to'] = self.env['ir.config_parameter'].sudo().get_param('sr_notify_low_stock_product.notify_to')
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.min_qty_user_ids',
                                                         self.min_qty_user_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.min_qty_group_ids',
                                                         self.min_qty_group_ids.ids)
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.outgoing_mail_id',
                                                         self.outgoing_mail_id.id)
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.apply_min_qty_on',
                                                         self.apply_min_qty_on)
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.min_qty',
                                                         self.min_qty)
        self.env['ir.config_parameter'].sudo().set_param('sr_notify_low_stock_product.notify_to',
                                                         self.notify_to)
        return super(ResConfigSettings, self).set_values()
