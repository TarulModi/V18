# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.tools.misc import get_lang
from odoo.exceptions import UserError
from odoo import api, fields, models, _
from odoo.addons.mail.wizard.mail_compose_message import _reopen


class AccountMoveSendWizard(models.TransientModel):
    _inherit = 'account.move.send.wizard'

    def action_send_and_print(self, allow_fallback_pdf=False):
        """ Create invoice documents and send them."""
        self.ensure_one()
        self.env[self._context.get('active_model')].browse(self._context.get('active_id')).sent_mail = True
        if self.alerts:
            self._raise_danger_alerts(self.alerts)
        self._update_preferred_settings()
        attachments = self._generate_and_send_invoices(
            self.move_id,
            **self._get_sending_settings(),
            allow_fallback_pdf=allow_fallback_pdf,
        )
        if attachments and self.sending_methods and 'manual' in self.sending_methods:
            return self._action_download(attachments)
        else:
            return {'type': 'ir.actions.act_window_close'}
