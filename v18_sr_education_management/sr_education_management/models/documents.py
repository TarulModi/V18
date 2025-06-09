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
from odoo.exceptions import ValidationError
import mimetypes

class Documents(models.Model):
    _name = "documents.documents"
    _inherit = ['mail.thread']
    _description = "Documents"
    _rec_name = "name"

    admission_id = fields.Many2one("admission.admission", string="Admission", tracking=True, copy=False)
    name = fields.Char("Name", tracking=True, required=True)
    documents = fields.Binary("Documents", attachment=True, required=True)
    document_filename = fields.Char("Document File Name")
    student_id = fields.Many2one("student.student", string="Student", tracking=True, copy=False)
    is_verified = fields.Boolean("Is Verified?")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._validate_file_type(vals.get('document_filename'))
        return super().create(vals_list)

    def write(self, vals):
        if 'document_filename' in vals:
            self._validate_file_type(vals.get('document_filename'))
        return super().write(vals)

    def _validate_file_type(self, filename):
        if filename:
            mime, _ = mimetypes.guess_type(filename)
            if not (mime and (mime.startswith('image/') or mime == 'application/pdf')):
                raise ValidationError("Only image files and PDF documents are allowed.")

    def action_open_viewer(self):
        self.ensure_one()
        if not self.documents:
            raise ValidationError("No document to preview.")
        query = """
                SELECT id
                FROM ir_attachment
                WHERE res_model = %s AND res_id = %s
                LIMIT 1
            """
        self.env.cr.execute(query, (self._name, self.id))
        result = self.env.cr.fetchone()
        attachment = self.env['ir.attachment'].browse(result)
        attachment.public = True
        return {
            'type': 'ir.actions.act_window',
            'name': 'Preview',
            'res_model': 'doc.preview',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_attachment_id': attachment.id,
            }
        }

    def unlink(self):
        for rec in self:
            if rec.admission_id and rec.is_verified and rec.student_id:
                raise ValidationError(_("You can not delete verified documents."))
        return super(Documents, self).unlink()
