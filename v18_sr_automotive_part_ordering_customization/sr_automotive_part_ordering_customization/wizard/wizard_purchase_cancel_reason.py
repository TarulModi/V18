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


class wizardPurchaseCancelReason(models.TransientModel):
    _name = 'wizard.purchase.cancel.reason'
    _desciption = 'Purchase Cancel Reason wizard'

    cancel_reason_id = fields.Many2one('purchase.cancel.reason', 'Cancel Reason')

    def action_cancel_po(self):
        if self.env.context.get('active_id'):
            purchase_id = self.env['purchase.order'].browse(self.env.context.get('active_id'))
            if purchase_id:
                purchase_id.cancel_reason_id = self.cancel_reason_id
                purchase_id.write({'state': 'cancel', 'mail_reminder_confirmed': False})
