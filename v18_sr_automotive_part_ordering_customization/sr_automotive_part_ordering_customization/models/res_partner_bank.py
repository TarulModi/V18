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


class PartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    account_type = fields.Selection([
        ('saving', 'Saving'),
        ('current', 'Current'),
        ('fixed_deposit', 'Fixed Deposit'),
    ], "Account Type")
    status = fields.Selection([
        ('Created', 'Created'),
        ('Verified', 'Verified'),
    ], default="Created", string="Status")
    ifsc_code = fields.Char('IFSC Code')
    image = fields.Binary("Cancel Check Photo")
