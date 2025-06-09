# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, _


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    def _action_send_mail(self, auto_commit=False):
        if self.env.context.get('mark_so_as_sent') and self.model == 'sale.order':
            self = self.with_context(mail_notify_author=self.env.user.partner_id in self.partner_ids)
            self.env[self._context.get('active_model')].browse(self._context.get('active_id')).sent_mail = True
        if self.env.context.get('mark_rfq_as_sent') and self.model == 'purchase.order':
            self = self.with_context(mail_notify_author=self.env.user.partner_id in self.partner_ids)
            self.env[self._context.get('active_model')].browse(self._context.get('active_id')).sent_mail = True
        return super(MailComposeMessage, self)._action_send_mail(auto_commit=auto_commit)