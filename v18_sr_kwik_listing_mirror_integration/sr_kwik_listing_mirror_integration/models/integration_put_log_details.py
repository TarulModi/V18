# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _


class IntegrationPutLogDetails(models.Model):
    _name = "integration.put.log.details"
    _description = "Integration Put Log Details"
    _inherit = ['mail.thread']
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char('Name', copy=False, tracking=True)
    integration_name = fields.Char('Integration Name', copy=False, tracking=True)
    qty = fields.Float('Quantity', copy=False, tracking=True)
    date = fields.Char('Date', copy=False, tracking=True)