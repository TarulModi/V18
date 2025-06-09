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

class ProfitAndLossStatement(models.Model):
    _name = 'profit.loss.statement'
    _description = 'Profit Loss Statement'
    _rec_name = 'name'

    name = fields.Char(default="Profit Loss Statement")
    non_operating_expenses = fields.Many2many('account.account',string='Non Operating Expenses')
    profit_loss_statement_ids = fields.One2many('profit.loss.statement.line','profit_loss_id',string='Profit Loss Statements')
