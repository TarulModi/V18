# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import re


class ResCompany(models.Model):
    _inherit = 'res.company'

    experience_letter_image = fields.Image(string="Experience Letter Image" )

    experience_letter_content = fields.Html(string="Experience Letter Content", encoding='utf-8')

    @api.constrains('experience_letter_content')
    def _check_dynamic_placeholders(self):
        employee_fields = self.env['hr.employee']._fields
        allowed_placeholders = set(employee_fields.keys())

        for record in self:
            content = record.experience_letter_content or ''
            raw_placeholders = re.findall(r'\[([^\[\]]+)\]', content)
            used_placeholders = set()

            for placeholder in raw_placeholders:
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', placeholder):
                    raise ValidationError(_(
                        "Invalid placeholder format: [%s].\n\n"
                        "Allowed format: Only letters, numbers, and underscores. No dots or symbols."
                    ) % placeholder)
                used_placeholders.add(placeholder)
            invalid_placeholders = used_placeholders - allowed_placeholders

            if invalid_placeholders:
                raise ValidationError(
                    "The HR Employee field Are Invalid.")