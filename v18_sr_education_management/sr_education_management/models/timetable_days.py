# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import calendar
from odoo import api, fields, models, _


class TimetableDays(models.Model):
    _name = "timetable.days"
    _inherit = ['mail.thread']
    _description = "Timetable Days"
    _rec_name = "day"

    timetable_id = fields.Many2one("school.timetable", string="Timetable", tracking=True)
    employee_id = fields.Many2one('hr.employee', string='Faculty', tracking=True, domain=[('is_faculty', '=', True)])
    subject_id = fields.Many2one('subject.subject', 'Subject', tracking=True)
    start_time = fields.Float("Start Time", tracking=True)
    end_time = fields.Float("End Time", tracking=True)
    class_room_id = fields.Many2one('class.room', 'Classroom', tracking=True)
    day = fields.Selection([
        ('0', calendar.day_name[0]),
        ('1', calendar.day_name[1]),
        ('2', calendar.day_name[2]),
        ('3', calendar.day_name[3]),
        ('4', calendar.day_name[4]),
        ('5', calendar.day_name[5]),
        ('6', calendar.day_name[6]),
    ], 'Day', tracking=True)
    course_id = fields.Many2one("courses.courses", string="course", related="timetable_id.course_id")
    academic_terms_id = fields.Many2one("academic.terms", string="Academic Term", related="timetable_id.academic_terms_id")
