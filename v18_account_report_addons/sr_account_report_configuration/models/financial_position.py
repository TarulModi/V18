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


class FinancialPosition(models.Model):
    _name = 'financial.position'
    _description = 'Financial Position Details'
    _res_name = 'name'

    name = fields.Char(default='Financial Position')
    financial_position_ids = fields.One2many('financial.position.line','financial_position_id',string='Financial Position')
    equity_liabilities_ids = fields.One2many('equity.liabilities.line','financial_position_id',string='Equity Liabilities')