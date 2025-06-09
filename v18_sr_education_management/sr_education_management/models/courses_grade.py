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


class CoursesGrade(models.Model):
    _name = "courses.grade"
    _inherit = ['mail.thread']
    _description = "Courses Grade"
    _rec_name = "grade_id"

    courses_id = fields.Many2one("courses.courses", tracking=True)
    grade_id = fields.Many2one("grade.grade", tracking=True)
    gpa = fields.Float(string="GPA", tracking=True)
    min_per = fields.Float(string="Minimum Percentage", tracking=True)
    max_per = fields.Float(string="Maximum Percentage", tracking=True)

    @api.onchange('grade_id')
    def onchange_grade_id(self):
        """
        When the grade_id field changes, automatically update the GPA,
        minimum percentage, and maximum percentage fields based on the selected grade.
        """
        for record in self:
            record.gpa = record.grade_id.gpa
            record.min_per = record.grade_id.min_per
            record.max_per = record.grade_id.max_per
