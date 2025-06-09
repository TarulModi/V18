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


class FinancialPositionLine(models.Model):
    _name = 'financial.position.line'
    _description = 'Financial Position Details'
    _rec_name = 'assets'

    financial_position_id = fields.Many2one('financial.position')
    assets = fields.Selection([('non_current_assets','Non-Current Assets'),
                               ('current_assets','Current Assets')],
                                string='Assets')

    account_ids = fields.Many2many('account.account',string='Financial Position Account')