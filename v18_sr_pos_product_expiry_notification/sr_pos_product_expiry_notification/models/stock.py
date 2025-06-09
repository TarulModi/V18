# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import base64
import itertools
import logging
from ast import literal_eval
from odoo import _, api, fields, models, tools, Command
from odoo.osv import expression
from odoo.exceptions import ValidationError, UserError
from odoo.tools import is_html_empty
from odoo.tools.safe_eval import safe_eval, time

_logger = logging.getLogger(__name__)


class MailTemplate(models.Model):
    _inherit = "mail.template"
    
    # def send_mail(self, res_id, force_send=False, raise_exception=False, email_values=None, notif_layout=False):
    #     """ Generates a new mail.mail. Template is rendered on record given by
    #     res_id and model coming from template.
    #
    #     :param int res_id: id of the record to render the template
    #     :param bool force_send: send email immediately; otherwise use the mail
    #         queue (recommended);
    #     :param dict email_values: update generated mail with those values to further
    #         customize the mail;
    #     :param str notif_layout: optional notification layout to encapsulate the
    #         generated email;
    #     :returns: id of the mail.mail that was created """
    #     self.ensure_one()
    #     Mail = self.env['mail.mail']
    #     Attachment = self.env['ir.attachment']  # TDE FIXME: should remove dfeault_type from context
    #
    #     # create a mail_mail based on values, without attachments
    #     values = self.generate_email(res_id)
    #     values['recipient_ids'] = [(4, pid) for pid in values.get('partner_ids', list())]
    #     values.update(email_values or {})
    #     attachment_ids = values.pop('attachment_ids', [])
    #     attachments = values.pop('attachments', [])
    #     # add a protection against void email_from
    #     if 'email_from' in values and not values.get('email_from'):
    #         values.pop('email_from')
    #     # encapsulate body
    #     if notif_layout and values['body_html']:
    #         try:
    #             template = self.env.ref(notif_layout, raise_if_not_found=True)
    #         except ValueError:
    #             _logger.warning('QWeb template %s not found when sending template %s. Sending without layouting.' % (notif_layout, self.name))
    #         else:
    #             record = self.env[self.model].browse(res_id)
    #             template_ctx = {
    #                 'message': self.env['mail.message'].sudo().new(dict(body=values['body_html'], record_name=record.display_name)),
    #                 'model_description': self.env['ir.model']._get(record._name).display_name,
    #                 'company': 'company_id' in record and record['company_id'] or self.env.user.company_id,
    #             }
    #             body = template.render(template_ctx, engine='ir.qweb', minimal_qcontext=True)
    #             values['body_html'] = self.env['mail.thread']._replace_local_links(body)
    #     if self.env.context.get('uid'):
    #         print ("=======custom")
    #         values.update({'author_id':self.env['res.users'].browse(self.env.context.get('uid')).partner_id.id})
    #     mail = Mail.create(values)
    #
    #     # manage attachments
    #     for attachment in attachments:
    #         attachment_data = {
    #             'name': attachment[0],
    #             'datas_fname': attachment[0],
    #             'datas': attachment[1],
    #             'type': 'binary',
    #             'res_model': 'mail.message',
    #             'res_id': mail.mail_message_id.id,
    #         }
    #         attachment_ids.append(Attachment.create(attachment_data).id)
    #     if attachment_ids:
    #         values['attachment_ids'] = [(6, 0, attachment_ids)]
    #         mail.write({'attachment_ids': [(6, 0, attachment_ids)]})
    #
    #     if force_send:
    #         mail.send(raise_exception=raise_exception)
    #     return mail.id  # TDE CLEANME: return mail + api.returns ?

    @api.returns('self', lambda value: value.ids)
    def send_mail_batch(self, res_ids, force_send=False, raise_exception=False, email_values=None,
                        email_layout_xmlid=False):
        """ Generates new mail.mails. Batch version of 'send_mail'.'

        :param list res_ids: IDs of modelrecords on which template will be rendered

        :returns: newly created mail.mail
        """
        # Grant access to send_mail only if access to related document
        self.ensure_one()
        self._send_check_access(res_ids)
        sending_email_layout_xmlid = email_layout_xmlid or self.email_layout_xmlid

        mails_sudo = self.env['mail.mail'].sudo()
        batch_size = int(
            self.env['ir.config_parameter'].sudo().get_param('mail.batch_size')
        ) or 50  # be sure to not have 0, as otherwise no iteration is done
        RecordModel = self.env[self.model].with_prefetch(res_ids)
        record_ir_model = self.env['ir.model']._get(self.model)

        for res_ids_chunk in tools.split_every(batch_size, res_ids):
            res_ids_values = self._generate_template(
                res_ids_chunk,
                ('attachment_ids',
                 'auto_delete',
                 'body_html',
                 'email_cc',
                 'email_from',
                 'email_to',
                 'mail_server_id',
                 'model',
                 'partner_to',
                 'reply_to',
                 'report_template_ids',
                 'res_id',
                 'scheduled_date',
                 'subject',
                 )
            )
            values_list = [res_ids_values[res_id] for res_id in res_ids_chunk]

            # get record in batch to use the prefetch
            records = RecordModel.browse(res_ids_chunk)
            attachments_list = []

            # lang and company is used for rendering layout
            res_ids_langs, res_ids_companies = {}, {}
            if sending_email_layout_xmlid:
                if self.lang:
                    res_ids_langs = self._render_lang(res_ids_chunk)
                res_ids_companies = records._mail_get_companies(default=self.env.company)

            for record in records:
                values = res_ids_values[record.id]
                values['recipient_ids'] = [(4, pid) for pid in (values.get('partner_ids') or [])]
                values['attachment_ids'] = [(4, aid) for aid in (values.get('attachment_ids') or [])]
                values.update(email_values or {})

                # delegate attachments after creation due to ACL check
                attachments_list.append(values.pop('attachments', []))

                # add a protection against void email_from
                if 'email_from' in values and not values.get('email_from'):
                    values.pop('email_from')

                # encapsulate body
                if not sending_email_layout_xmlid:
                    values['body'] = values['body_html']
                    continue

                lang = res_ids_langs.get(record.id) or False
                company = res_ids_companies.get(record.id) or self.env.company
                model_lang = record_ir_model.with_context(lang=lang) if lang else record_ir_model

                template_ctx = {
                    # message
                    'message': self.env['mail.message'].sudo().new(
                        dict(body=values['body_html'], record_name=record.display_name)),
                    'subtype': self.env['mail.message.subtype'].sudo(),
                    # record
                    'model_description': model_lang.display_name,
                    'record': record,
                    'record_name': False,
                    'subtitles': False,
                    # user / environment
                    'company': company,
                    'email_add_signature': False,
                    'signature': '',
                    'website_url': '',
                    # tools
                    'is_html_empty': is_html_empty,
                }
                body = model_lang.env['ir.qweb']._render(sending_email_layout_xmlid, template_ctx,
                                                         minimal_qcontext=True, raise_if_not_found=False)
                if not body:
                    _logger.warning(
                        'QWeb template %s not found when sending template %s. Sending without layout.',
                        sending_email_layout_xmlid,
                        self.name,
                    )
                    body = values['body_html']

                values['body_html'] = self.env['mail.render.mixin']._replace_local_links(body)
                values['body'] = values['body_html']

                # Added custom code
                if self.env.context.get('uid'):
                    values.update({'author_id': self.env['res.users'].browse(self.env.context.get('uid')).partner_id.id})
                ####

            mails = self.env['mail.mail'].sudo().create(values_list)

            # manage attachments
            for mail, attachments in zip(mails, attachments_list):
                if attachments:
                    attachments_values = [
                        (0, 0, {
                            'name': name,
                            'datas': datas,
                            'type': 'binary',
                            'res_model': 'mail.message',
                            'res_id': mail.mail_message_id.id,
                        })
                        for (name, datas) in attachments
                    ]
                    mail.with_context(default_type=None).write({'attachment_ids': attachments_values})

            mails_sudo += mails

        if force_send:
            mails_sudo.send(raise_exception=raise_exception)
        return mails_sudo



# class CustomProductionLot(models.Model):
#     _inherit = "stock.production.lot"
#
#     @api.model
#     def validate_serial_lot_number(self, numbers, pos_config_id):
#         result = self.search([('name', 'in', numbers)]).filtered(lambda x: x.product_expiry_alert)
#         return bool(result)
#
#     def update_expiry_state(self):
#         current_date = fields.Date.from_string(fields.Date.today())
#         all_records = self.search([])
#         all_expired_lot_serial_records = all_records.filtered(lambda x: fields.Date.from_string(x.alert_date) == current_date)
#         all_expired_lot_serial_records.write({
#             'product_expiry_alert': True,
#         })
#         if all_expired_lot_serial_records:
#             inventory_managers = self.env['res.users'].search([]).filtered(lambda user: user.has_group('stock.group_stock_manager'))
#             if inventory_managers:
#                 user_emails = [user.email for user in inventory_managers]
#                 if user_emails:
#                     template = self.env.ref('sr_pos_product_expiry_notification.stock_production_lot_expired_email')
#                     template_id = self.env['mail.template'].browse(template.id);
#                     template_id.with_context(email_to=user_emails, lot_ids=all_expired_lot_serial_records).send_mail(False, force_send=True)


class CustomProductionLot(models.Model):
    _inherit = "stock.lot"

    @api.model
    def check_lot_expiry_alert(self, args):
        result = self.sudo().search([('name', '=', args['lot_no'])],limit=1)
        expired = False
        if result and result.alert_date:
            if result.alert_date < fields.Datetime.now():
                expired = True
        return expired

    def update_expiry_state(self):
        current_date = fields.Date.from_string(fields.Date.today())
        all_records = self.search([])
        all_expired_lot_serial_records = all_records.filtered(lambda x: fields.Date.from_string(x.alert_date) == current_date)
        all_expired_lot_serial_records.write({
            'product_expiry_alert': True,
        })
        if all_expired_lot_serial_records:
            inventory_managers = self.env['res.users'].search([]).filtered(lambda user: user.has_group('stock.group_stock_manager'))
            if inventory_managers:
                user_emails = [user.email for user in inventory_managers]
                if user_emails:
                    template = self.env.ref('sr_pos_product_expiry_notification.stock_production_lot_expired_email')
                    template_id = self.env['mail.template'].browse(template.id);
                    template_id.with_context(email_to=user_emails, lot_ids=all_expired_lot_serial_records).send_mail(False, force_send=True)
