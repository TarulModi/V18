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


class CashFlowsIndirect(models.Model):
    _name = 'cash.flows.indirect'
    _description = 'Cash Flows Indirect'
    _rec_name = 'name'

    name = fields.Char(default='Cash Flows')
    cash_flow_ids = fields.One2many('cash.flows.indirect.line',
                                    'cash_flow_id',
                                    string='Cash Flow')