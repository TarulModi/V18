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


class Subject(models.Model):
    _name = "subject.subject"
    _inherit = ['mail.thread']
    _description = "Subject"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    code = fields.Char(string="Code", tracking=True)
    type = fields.Selection([('theory', 'Theory'), ('practical', 'Practical'), ('both', 'Both'), ('other', 'Other')],
                            string="Type", tracking=True, default="theory")
    parent_id = fields.Many2one("subject.subject", tracking=True)
    courses_id = fields.Many2one("courses.courses", tracking=True)
    subject_type = fields.Selection([('compulsory', 'Compulsory'), ('elective', 'Elective')],
                                    string="Subject Type", tracking=True, default="compulsory")

    @api.model
    def default_get(self, fields_list):
        """
        Override default_get to set default courses_id from context, if available.
        This allows automatic assignment of the course when creating a subject from a related course view.
        """
        res = super(Subject, self).default_get(fields_list)
        if self.env.context.get('default_courses_id'):
            res['courses_id'] = self.env.context.get('default_courses_id')
        return res
