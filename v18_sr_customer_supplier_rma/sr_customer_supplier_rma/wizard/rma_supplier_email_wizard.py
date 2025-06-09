from odoo import models, api, _
import base64

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        rma_id = self.env.context.get('default_rma_ids')
        print("------rma_id------",rma_id)
        if rma_id:
            rma = self.env['rma.supplier'].browse(rma_id)
            print("------rma----rma--", rma)
            partner_name = rma.purchase_order_id.partner_id.name or "Customer"
            order_name = rma.name or "RMA"
            print("------rma----order_name--", order_name)
            subject = rma.subject or "No Subject"
            print("------rma----subject--", subject)
            date = rma.date.strftime('%B %d, %Y') if rma.date else "Unknown Date"
            state = rma.status or "Unknown"
            print("------rma----state--", state)

            body = f"""
                <p>Dear <strong>{partner_name}</strong>,</p>
                <p>Your RMA Supplier <strong>{order_name}</strong> with subject "<em>{subject}</em>" 
                created on <strong>{date}</strong> is currently in the <strong>{state}</strong> state.</p>
                <p>Thank you.</p>
            """

            res.update({
                'subject': f"{subject}",
                'body': body,
                'partner_ids': [(6, 0, [rma.purchase_order_id.partner_id.id])],
                'model': 'rma.supplier',
                'composition_mode': 'comment',
            })
        return res

    @api.depends('composition_mode', 'model', 'res_domain', 'res_ids', 'template_id')
    def _compute_attachment_ids(self):
        super()._compute_attachment_ids()
        for composer in self:
            if composer.model == 'rma.supplier' and composer.composition_mode == 'comment':
                res_ids = composer._evaluate_res_ids() or []
                if len(res_ids) != 1:
                    continue

                rma = self.env['rma.supplier'].browse(res_ids[0])
                report = self.env.ref('sr_customer_supplier_rma.report_rma_supplier')
                pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(
                    report.report_name, [rma.id]
                )
                pdf_base64 = base64.b64encode(pdf_content)
                attachment = self.env['ir.attachment'].create({
                    'name': f'RMA_Supplier_{rma.name}.pdf',
                    'type': 'binary',
                    'datas': pdf_base64,
                    'res_model': rma._name,
                    'res_id': rma.id,
                    'mimetype': 'application/pdf',
                })
                composer.attachment_ids = [(4, attachment.id)]
