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


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sent_mail = fields.Boolean(string="Sent Email", copy=False)


class SendMassMailPurchase(models.TransientModel):
    _name = "send.mass.mail.purchase"

    @api.model
    def _get_template_id(self):
        temp_id = self.env["mail.template"].search([("name", "=", "Purchase: Purchase Order")])
        if temp_id:
            return temp_id[0]
        return

    template_id = fields.Many2one(
        "mail.template", string="Template", default=_get_template_id, required=True
    )

    def send_mass_mail(self):
        purchase_order_id = self.env["purchase.order"].browse(
            self._context.get("active_ids")
        )
        for record in purchase_order_id:
            if not record.partner_id.email:
                raise UserError(_("Please Define Email in this partner and try again : %s")% record.partner_id.name)
        if self.template_id.id:
            template = self.template_id
            message_composer = (
                self.env["mail.compose.message"]
                .with_context(
                    default_res_model="purchase.order",
                    default_use_template=bool(template),
                    mark_rfq_as_sent=True,
                    custom_layout="mail.mail_notification_paynow",
                    force_email=True,
                )
                .create(
                    {
                        "template_id": template and template.id or False,
                        "model": "purchase.order",
                        "composition_mode": "comment",
                    }
                )
            )._action_send_mail()
            purchase_order_id.sent_mail = True
