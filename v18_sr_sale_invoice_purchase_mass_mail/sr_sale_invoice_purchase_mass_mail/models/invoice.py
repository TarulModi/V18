# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.exceptions import UserError
from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.move"

    sent_mail = fields.Boolean(string="Sent Email", copy=False)


class SendMassMailInvoice(models.TransientModel):
    _name = "send.mass.mail.invoice"
    _description = "Send Mass Mail Invoice"

    @api.model
    def _get_template_id(self):
        temp_id = self.env["mail.template"].search([("name", "=", "Invoice: Sending")])
        if temp_id:
            return temp_id[0]
        return

    template_id = fields.Many2one(
        "mail.template", string="Template", default=_get_template_id, required=True
    )

    def send_mass_mail(self):
        invoice_order_id = self.env["account.move"].browse(
            self._context.get("active_ids")
        )
        for record in invoice_order_id:
            if not record.partner_id.email:
                raise UserError(_("Please Define Email in this partner and try again : %s")% record.partner_id.name)
        if self.template_id.id:
            template = self.template_id
            message_composer = (
                self.env["mail.compose.message"]
                .with_context(
                    default_res_model="account.move",
                    default_use_template=bool(template),
                    mark_invoice_as_sent=True,
                    custom_layout="mail.mail_notification_paynow",
                    force_email=True,
                )
                .create(
                    {
                        "template_id": template and template.id or False,
                        "model": "account.move",
                        "composition_mode": "comment",
                    }
                )
            )._action_send_mail()
            invoice_order_id.sent_mail = True
