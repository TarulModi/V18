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


class EquityLiabilitiesLine(models.Model):
    _name = 'equity.liabilities.line'
    _description = 'Equity Liabilities Details'

    financial_position_id = fields.Many2one('financial.position')
    equity_liabilities =fields.Selection([('equity','Equity'),
                                          ('non_current_liabilities','Non Current Liabilities'),
                                          ('current_liabilities','Current Liabilities')],
                                         string='Equity Liabilities')
    account_ids = fields.Many2many('account.account', string='Equity Liabilities  Account')
