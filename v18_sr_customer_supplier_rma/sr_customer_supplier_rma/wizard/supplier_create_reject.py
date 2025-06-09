# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api
from odoo.exceptions import UserError


class RejectWizard(models.TransientModel):
    _name = 'reject.wizard'
    _description = 'Reject Wizard'

    reject_reason_id = fields.Many2one('rma.supplier.reason', string='Reject Reason', required=True)

    def create_reject(self):
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        records = self.env[active_model].browse(active_ids)

        for record in records:
            if record.status not in ['draft', 'approved', 'processing']:
                raise UserError("Only records in Draft, Approved, or Processing status can be rejected.")

            record.write({
                'status': 'reject',
                'reject_reason_id': self.reject_reason_id.id
            })

        return {'type': 'ir.actions.act_window_close'}
