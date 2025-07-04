# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BuyMembershipWizard(models.TransientModel):
    _name = "buy.membership.wizard"
    _description = "Buy Membership Wizard"

    membership_id = fields.Many2one("gym.membership", string="Membership")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    fees = fields.Float("Fees")

    @api.onchange('membership_id')
    def _onchange_membership(self):
        if self.membership_id:
            self.fees = self.membership_id.fees
            self.start_date = self.membership_id.start_date
            self.end_date = self.membership_id.end_date

    def create_membership_invoice(self):
        active_id = self.env['res.partner'].browse(self._context.get('active_id'))
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': active_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.membership_id.name,
                'quantity': 1,
                'price_unit': self.fees,
            })],
        })

        self.env['gym.member.membership'].create({
            'partner_id': active_id.id,
            'membership_id': self.membership_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'fees': self.fees,
            'status': 'confirm',
        })

        self.membership_id.partner_ids = [(4, active_id.id)]
        active_id.invoice_ids = [(4, invoice.id)]

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
