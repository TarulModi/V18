# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    joining_date = fields.Date(string='Joining Date')
    last_working_date = fields.Date(string='Last Working Date')
    letter_issue_date = fields.Date(string="Letter Issue  Date", default=fields.Date.context_today, required=True)