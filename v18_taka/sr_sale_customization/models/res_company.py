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


class company(models.Model):
    _inherit = 'res.company'

    insufficient_stock_email_user_ids = fields.Many2many('res.users',
        'company_user_rel', 'company_id', 'user_id',
        string="Insufficient Stock Email Users")
