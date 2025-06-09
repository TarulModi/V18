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


class Partner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved')
    ], string="Status", default="draft")

    def action_approve(self):
        self.state = 'approved'
