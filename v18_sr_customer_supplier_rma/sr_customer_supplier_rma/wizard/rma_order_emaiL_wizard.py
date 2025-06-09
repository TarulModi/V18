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
from odoo import models, api, _


class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        rma_id = self.env.context.get('default_rma_ids')
        active_model = self.env.context.get('default_model')

        if rma_id and active_model in ['rma.order', 'rma.supplier']:
            rma = self.env[active_model].browse(rma_id)
            partner, subject, order_name, date, state = self._prepare_rma_details(rma, active_model)

            body = f"""
                <p>Dear <strong>{partner.name}</strong>,</p>
                <p>Your RMA Order <strong>{order_name}</strong> with subject "<em>{subject}</em>" 
                created on <strong>{date}</strong> is currently in the <strong>{state}</strong> state.</p>
                <p>Thank you.</p>
            """

            res.update({
                'subject': f"{subject}",
                'body': body,
                'partner_ids': [(6, 0, [partner.id])],
                'model': active_model,
                'composition_mode': 'comment',
            })

        return res

    def _prepare_rma_details(self, rma, active_model):
        if active_model == 'rma.order':
            partner = rma.sale_order_id.partner_id
            state = rma.state or "Unknown"
        else:  # 'rma.supplier'
            partner = rma.purchase_order_id.partner_id
            state = rma.status or "Unknown"

        subject = rma.subject or "No Subject"
        order_name = rma.name or "RMA"
        date = rma.date.strftime('%B %d, %Y') if rma.date else "Unknown Date"
        return partner, subject, order_name, date, state

    @api.depends('composition_mode', 'model', 'res_domain', 'res_ids', 'template_id')
    def _compute_attachment_ids(self):
        super()._compute_attachment_ids()

        for composer in self:
            if composer.composition_mode != 'comment':
                continue

            res_ids = composer._evaluate_res_ids() or []
            if len(res_ids) != 1:
                continue

            model = composer.model
            if model not in ['rma.order', 'rma.supplier']:
                continue

            rma = self.env[model].browse(res_ids[0])
            report_ref = 'sr_customer_supplier_rma.report_rma_order' if model == 'rma.order' else 'sr_customer_supplier_rma.report_rma_supplier'
            report = self.env.ref(report_ref)

            pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report.report_name, [rma.id])
            pdf_base64 = base64.b64encode(pdf_content)

            attachment = self.env['ir.attachment'].create({
                'name': f'RMA_{rma._name.replace(".", "_").title()}_{rma.name}.pdf',
                'type': 'binary',
                'datas': pdf_base64,
                'res_model': rma._name,
                'res_id': rma.id,
                'mimetype': 'application/pdf',
            })
            composer.attachment_ids = [(4, attachment.id)]


# from odoo import models, api, _
# import base64
#
# class MailComposeMessage(models.TransientModel):
#     _inherit = 'mail.compose.message'
#
#     @api.model
#     def default_get(self, fields_list):
#         res = super().default_get(fields_list)
#         rma_id = self.env.context.get('default_rma_ids')
#         active_model = self.env.context.get('default_model')
#         print("---active_model----------",active_model)
#         if rma_id:
#             if active_model == 'rma.order':
#                 rma = self.env[active_model].browse(rma_id)
#                 partner_name = rma.sale_order_id.partner_id.name or "Customer"
#                 order_name = rma.name or "RMA"
#                 subject = rma.subject or "No Subject"
#                 date = rma.date.strftime('%B %d, %Y') if rma.date else "Unknown Date"
#                 state = rma.state or "Unknown"
#                 partner_ids = [rma.sale_order_id.partner_id.id]
#
#             if active_model == 'rma.supplier':
#                 rma = self.env[active_model].browse(rma_id)
#                 print("------rma----rma--", rma)
#                 partner_name = rma.purchase_order_id.partner_id.name or "Customer"
#                 order_name = rma.name or "RMA"
#                 print("------rma----order_name--", order_name)
#                 subject = rma.subject or "No Subject"
#                 print("------rma----subject--", subject)
#                 date = rma.date.strftime('%B %d, %Y') if rma.date else "Unknown Date"
#                 state = rma.status or "Unknown"
#                 print("------rma----state--", state)
#                 partner_ids = [rma.purchase_order_id.partner_id.id]
#
#             body = f"""
#                     <p>Dear <strong>{partner_name}</strong>,</p>
#                     <p>Your RMA Order <strong>{order_name}</strong> with subject "<em>{subject}</em>"
#                     created on <strong>{date}</strong> is currently in the <strong>{state}</strong> state.</p>
#                     <p>Thank you.</p>
#                 """
#
#             res.update({
#                 'subject': f"{subject}",
#                 'body': body,
#                 'partner_ids': [(6, 0, partner_ids)],
#                 'model': active_model,
#                 'composition_mode': 'comment',
#             })
#         return res
#
#     @api.depends('composition_mode', 'model', 'res_domain', 'res_ids', 'template_id')
#     def _compute_attachment_ids(self):
#         super()._compute_attachment_ids()
#         for composer in self:
#             if composer.model == 'rma.order' and composer.composition_mode == 'comment':
#                 res_ids = composer._evaluate_res_ids() or []
#                 if len(res_ids) != 1:
#                     continue
#
#                 rma = self.env['rma.order'].browse(res_ids[0])
#                 report = self.env.ref('sr_customer_supplier_rma.report_rma_order')
#
#                 pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
#                     report.report_name, [rma.id]
#                 )
#                 pdf_base64 = base64.b64encode(pdf_content)
#                 attachment = self.env['ir.attachment'].create({
#                     'name': f'RMA_Order_{rma.name}.pdf',
#                     'type': 'binary',
#                     'datas': pdf_base64,
#                     'res_model': rma._name,
#                     'res_id': rma.id,
#                     'mimetype': 'application/pdf',
#                 })
#                 composer.attachment_ids = [(4, attachment.id)]
#
#             if composer.model == 'rma.supplier' and composer.composition_mode == 'comment':
#                 res_ids = composer._evaluate_res_ids() or []
#                 if len(res_ids) != 1:
#                     continue
#
#                 rma = self.env['rma.supplier'].browse(res_ids[0])
#                 report = self.env.ref('sr_customer_supplier_rma.report_rma_supplier')
#                 pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
#                     report.report_name, [rma.id]
#                 )
#                 pdf_base64 = base64.b64encode(pdf_content)
#                 attachment = self.env['ir.attachment'].create({
#                     'name': f'RMA_Supplier_{rma.name}.pdf',
#                     'type': 'binary',
#                     'datas': pdf_base64,
#                     'res_model': rma._name,
#                     'res_id': rma.id,
#                     'mimetype': 'application/pdf',
#                 })
#                 composer.attachment_ids = [(4, attachment.id)]
