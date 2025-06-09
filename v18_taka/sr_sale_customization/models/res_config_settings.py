# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    insufficient_stock_email_user_ids = fields.Many2many('res.users',
        related="company_id.insufficient_stock_email_user_ids",
        string="Insufficient Stock Email Users",
        readonly=False)
