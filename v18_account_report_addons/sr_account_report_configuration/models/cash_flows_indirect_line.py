# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _


class CashFlowsIndirectLine(models.Model):
    _name = 'cash.flows.indirect.line'
    _description = 'Cash Flows Indirect Details'
    _rec_name = 'name'

    name = fields.Char(default='Cash Flows')
    cash_flow_id = fields.Many2one('cash.flows.indirect')
    cash_flow = fields.Selection([
        ('operating_activities', 'Operating Activities'),
        ('change_operating_liabilities', 'Changes in Operating Assets And Liabilities'),
        ('investing_activities', 'Investing Activities'),
        ('financing_activities', 'Financing Activities'),
        ('cash_equivalents', 'Cash and Cash Equivalents')
    ], string="Cash Flow Type")

    operating_activities_ids = fields.Many2many('account.account', string='Operating Activities')


