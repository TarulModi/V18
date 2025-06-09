# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from html import unescape
from odoo import models, fields
import re


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date(string='Joining Date')
    last_working_date = fields.Date(string='Last Working Date')
    letter_issue_date = fields.Date(string="Letter Issue Date", default=fields.Date.context_today, required=True)

    def _safe_format_date(self, field_name):
        """Safely formats date field if exists."""
        value = getattr(self, field_name, False)
        return value.strftime('%d %B %Y') if value else ''

    def render_experience_letter_html(self):
        self.ensure_one()

        raw_html = self.company_id.experience_letter_content or ''
        clean_html = unescape(raw_html)  # Decode HTML entities like &nbsp;
        clean_html = clean_html.replace(u'\xa0', ' ')  # Replace non-breaking space with normal space
        clean_html = re.sub(r'[ \t]+', ' ', clean_html).strip()

        values = {}
        for field_name in self._fields:
            try:
                value = getattr(self, field_name)
                if isinstance(value, fields.Date):
                    value = self._safe_format_date(field_name)
                elif isinstance(value, models.Model):
                    value = value.name
                values[field_name] = value or ''
            except Exception:
                values[field_name] = ''

        def replacer(match):
            key = match.group(1)
            return str(values.get(key, f"[{key}]"))

        final_html = re.sub(r'\[([a-zA-Z_]+)\]', replacer, clean_html)

        return final_html.strip()
