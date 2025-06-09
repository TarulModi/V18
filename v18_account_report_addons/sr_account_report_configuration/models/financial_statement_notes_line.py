# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models,fields,api,_

class FinancialStatementNotesLine(models.Model):
    _name = 'financial.statement.notes.line'
    _description = 'Financial Statement Notes Line'

    payment_other_receivables = fields.Selection([
        ('trade_other_receivable','Trade and Other Receivable'),
        ('vat','Vat')
    ],string='Name')
    account_ids = fields.Many2many('account.account',string='Accounts')
    financial_id = fields.Many2one('financial.statement.notes',string='Financial')