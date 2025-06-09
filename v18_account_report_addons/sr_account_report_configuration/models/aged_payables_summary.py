# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields,models,api,_


class AgedPayablesSummary(models.Model):
    _name = 'aged.payables.summary'
    _description = 'Aged Payables Summary'
    _rec_name = 'name'

    name = fields.Char(default='Aged Payables')
    aged_payable_ids = fields.Many2many('account.account', string='Aged Payables Summary')