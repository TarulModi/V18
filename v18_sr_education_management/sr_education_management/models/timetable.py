# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import time
from odoo import api, fields, models, _


class TimeTable(models.Model):
    _name = "school.timetable"
    _inherit = ['mail.thread']
    _description = "TimeTable"
    _rec_name = "company_id"

    company_id = fields.Many2one("res.company", string="School", tracking=True, default=lambda self: self.env.company)
    course_id = fields.Many2one("courses.courses", string="course", tracking=True)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    academic_terms_id = fields.Many2one("academic.terms", string="Academic Term", tracking=True)
    start_date = fields.Date("Start Date", tracking=True, default=time.strftime('%Y-%m-01'))
    end_date = fields.Date("End Date", tracking=True)

    time_table_monday = fields.One2many(
        'timetable.days', 'timetable_id', 'Monday',
        domain=[('day', '=', '0')], tracking=True)
    time_table_tuesday = fields.One2many(
        'timetable.days', 'timetable_id', 'Tuesday',
        domain=[('day', '=', '1')], tracking=True)
    time_table_wednesday = fields.One2many(
        'timetable.days', 'timetable_id', 'Wednesday',
        domain=[('day', '=', '2')], tracking=True)
    time_table_thursday = fields.One2many(
        'timetable.days', 'timetable_id', 'Thursday',
        domain=[('day', '=', '3')], tracking=True)
    time_table_friday = fields.One2many(
        'timetable.days', 'timetable_id', 'Friday',
        domain=[('day', '=', '4')], tracking=True)
    time_table_saturday = fields.One2many(
        'timetable.days', 'timetable_id', 'Saturday',
        domain=[('day', '=', '5')], tracking=True)
    time_table_sunday = fields.One2many(
        'timetable.days', 'timetable_id', 'Sunday',
        domain=[('day', '=', '6')], tracking=True)