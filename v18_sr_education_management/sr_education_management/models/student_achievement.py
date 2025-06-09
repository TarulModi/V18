# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from email.policy import default

from odoo import api, fields, models, _


class StudentAchievement(models.Model):
    _name = "student.achievement"
    _inherit = ['mail.thread']
    _description = "Student Achievement"
    _rec_name = "name"

    student_id = fields.Many2one('student.student')
    admission_id = fields.Many2one('admission.admission')
    name = fields.Char(required=True, tracking=True, translate=True)
    achievement_date = fields.Date(required=True, tracking=True)
    date_end = fields.Date(tracking=True)
    description = fields.Html(string="Description", tracking=True, translate=True)
    documents = fields.Binary("Documents", tracking=True)