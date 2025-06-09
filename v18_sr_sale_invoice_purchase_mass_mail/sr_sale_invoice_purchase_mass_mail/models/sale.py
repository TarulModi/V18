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
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sent_mail = fields.Boolean(string="Sent Email", copy=False)


class SendMassMailSale(models.TransientModel):
    _name = "send.mass.mail.sale"

    @api.model
    def _get_template_id(self):
        temp_id = self.env["mail.template"].search(
            [("name", "=", "Sales: Send Quotation")]
        )
        if temp_id:
            return temp_id[0]
        return

    template_id = fields.Many2one(
        "mail.template", string="Template", default=_get_template_id, required=True
    )

    def send_mass_mail(self):
        sale_order_id = self.env["sale.order"].browse(self._context.get("active_ids"))
        for record in sale_order_id:
            if not record.partner_id.email:
                raise UserError(_("Please Define Email in this partner and try again : %s")% record.partner_id.name)
        if self.template_id.id:
            template = self.template_id
            message_composer = (
                self.env["mail.compose.message"]
                .with_context(
                    default_use_template=bool(template),
                    mark_so_as_sent=True,
                    custom_layout="mail.mail_notification_paynow",
                    proforma=self.env.context.get("proforma", False),
                    force_email=True,
                    mail_notify_author=True,
                )
                .create(
                    {
                        "model": "sale.order",
                        "template_id": template and template.id or False,
                        "composition_mode": "comment",
                    }
                )
            )._action_send_mail()
            sale_order_id.sent_mail = True
