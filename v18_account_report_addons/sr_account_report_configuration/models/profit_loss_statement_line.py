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


class ProfitAndLossStatementLine(models.Model):
    _name = 'profit.loss.statement.line'
    _description = 'Profit Loss Statement Line'

    operating_expenses = fields.Selection([
        ('general_administrative_expenses','General & Administrative Expenses'),
        ('factory_production_expenses','Factory & Production Expenses'),
        ('staff_cost','Staff Cost')
    ],string='Name')

    account_ids = fields.Many2many('account.account' , string='Accounts')
    profit_loss_id = fields.Many2one('profit.loss.statement',string='Profit Loss')