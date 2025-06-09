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


class DocPrview(models.TransientModel):
    _name = "doc.preview"
    _description = "Doc Preview"

    attachment_id = fields.Many2one("ir.attachment")
    preview_html = fields.Html(string="Preview", compute='_compute_preview_html', sanitize=False)

    @api.depends('attachment_id')
    def _compute_preview_html(self):
        for rec in self:
            if rec.attachment_id:
                rec.preview_html = f"""
                        <iframe src="/web/content/{rec.attachment_id.id}?download=false"
                                width="100%" height="200px" frameborder="0" style="min-height: 600px;"></iframe>
                    """
            else:
                rec.preview_html = "<p>No document to preview.</p>"

    def download_document(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self.attachment_id.id}?download=true',
            'target': 'self',
        }