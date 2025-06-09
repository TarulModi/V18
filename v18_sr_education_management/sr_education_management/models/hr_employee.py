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


class Employee(models.Model):
    _inherit = "hr.employee"

    is_faculty = fields.Boolean(string="Is Faculty", tracking=True)
    subject_ids = fields.One2many("employee.subject", "employee_id", string="Subjects")
    time_table_monday = fields.One2many(
        'timetable.days', 'employee_id', 'Monday',
        domain=[('day', '=', '0')], tracking=True)
    time_table_tuesday = fields.One2many(
        'timetable.days', 'employee_id', 'Tuesday',
        domain=[('day', '=', '1')], tracking=True)
    time_table_wednesday = fields.One2many(
        'timetable.days', 'employee_id', 'Wednesday',
        domain=[('day', '=', '2')], tracking=True)
    time_table_thursday = fields.One2many(
        'timetable.days', 'employee_id', 'Thursday',
        domain=[('day', '=', '3')], tracking=True)
    time_table_friday = fields.One2many(
        'timetable.days', 'employee_id', 'Friday',
        domain=[('day', '=', '4')], tracking=True)
    time_table_saturday = fields.One2many(
        'timetable.days', 'employee_id', 'Saturday',
        domain=[('day', '=', '5')], tracking=True)
    time_table_sunday = fields.One2many(
        'timetable.days', 'employee_id', 'Sunday',
        domain=[('day', '=', '6')], tracking=True)
