# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, SUPERUSER_ID


class srMassConfirmQuotation(models.TransientModel):
    _name = 'mass.confirm.quotation'
    _description = "Mass Confirm Quotation"

    is_send_email = fields.Boolean(string="Do you want to send Email?")
    template_id = fields.Many2one('mail.template', 'Use Template', domain=[('model_id', '=', 'sale.order')])

    @api.model
    def default_get(self, fields):
        result = super(srMassConfirmQuotation, self).default_get(fields)
        result['template_id'] = self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)
        return result

    def sr_mass_confirm_quotations(self):
        quotation_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
        for record in quotation_ids:
            if record.state in ['draft', 'sent']:
                record.action_confirm()
        return True

    def sr_mass_confirm_quotations_with_emails(self):
        quotation_ids = self.env['sale.order'].browse(self._context.get('active_ids'))
        if self.env.su:
            self = self.with_user(SUPERUSER_ID)
        for order in quotation_ids:
            order.action_confirm()
            order.with_context(force_send=True).message_post_with_source(
            self.template_id,
            email_layout_xmlid='mail.mail_notification_layout_with_responsible_signature',
            subtype_xmlid='mail.mt_comment',
        )
