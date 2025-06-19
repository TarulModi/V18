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


class IntegrationErrorLog(models.Model):
    _name = "integration.error.log"
    _description = "Integration Error Log"
    _inherit = ['mail.thread']
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char('Error Log', required=True, copy=False, tracking=True)
    integration_name = fields.Char('Integration Name', copy=False, tracking=True)
    remark = fields.Char('Remark', copy=False, tracking=True)
    date = fields.Char('Date', copy=False, tracking=True)

    def _log_integration_error(self, sku, integration_name, remark):
        self.env['integration.error.log'].create({
            'name': sku,
            'integration_name': integration_name,
            'remark': remark,
            'date': fields.Datetime.now(),
        })