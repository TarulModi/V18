# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, _


class srPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    payment_count = fields.Integer(
        string='Payment Count', compute='_get_advance_payment', readonly=True, copy=False
    )
    payment_ids = fields.One2many(
        'account.payment', 'purchase_order_id', string="Payments", readonly=True, copy=False
    )
    is_paid = fields.Boolean(string="Is Paid", copy=False)
    advance_payment = fields.Float("Advance Payment", copy=False)
    remaining_payment = fields.Float("Remaining Payment", copy=False)

    def action_register_purchase_advance_payment(self):
        return {
            'name': _('Register Advance Payment'),
            'res_model': 'account.purchase.advance.payment.register',
            'view_mode': 'form',
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def _get_advance_payment(self):
        for order in self:
            payment_ids = self.env['account.payment'].search(
                [('purchase_order_id', '=', order.id)]
            )
            order.payment_count = len(payment_ids)

    def action_view_payment(self):
        payments = self.env['account.payment'].search(
            [('purchase_order_id', '=', self.id)]
        )
        action = self.env["ir.actions.actions"]._for_xml_id(
            "account.action_account_payments_payable"
        )
        if len(payments) > 1:
            action['domain'] = [('id', 'in', payments.ids)]
        elif len(payments) == 1:
            form_view = [(self.env.ref('account.view_account_payment_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [
                    (state, view) for state, view in action['views'] if view != 'form'
                ]
            else:
                action['views'] = form_view
            action['res_id'] = payments.id
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
