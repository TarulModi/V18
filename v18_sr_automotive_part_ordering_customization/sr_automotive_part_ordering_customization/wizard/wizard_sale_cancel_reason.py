# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _


class wizardSaleCancelReason(models.TransientModel):
    _name = 'wizard.sale.cancel.reason'
    _desciption = 'Sale Cancel Reason wizard'

    cancel_reason_id = fields.Many2one('sale.cancel.reason', 'Cancel Reason')

    def action_cancel_so(self):
        if self.env.context.get('active_id'):
            sale_id = self.env['sale.order'].browse(self.env.context.get('active_id'))
            if sale_id:
                sale_id.cancel_reason_id = self.cancel_reason_id
                sale_id._action_cancel()
