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


class ClassRoom(models.Model):
    _name = "class.room"
    _inherit = ['mail.thread']
    _description = "Class Room"
    _rec_name = "name"

    # Basic Info
    name = fields.Char(string="Name", tracking=True, translate=True)
    division_id = fields.Many2one("division.division", string="Division", tracking=True)
    class_number = fields.Char(string="Class Number", tracking=True, translate=True)
    course_id = fields.Many2one("courses.courses", string="Course", tracking=True)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True,
                                       domain="[('academic_year_id', '=', academic_year_id), ('course_id', '=', course_id)]")

    # Teacher assignment
    employee_id = fields.Many2one("hr.employee", string="Teacher", tracking=True, domain=[('is_faculty', '=', True)])

    # Company/School Info
    company_id = fields.Many2one("res.company", string="School", tracking=True, default=lambda self: self.env.company)

    # Capacity & Assignment
    capacity = fields.Integer(string="Capacity", tracking=True)
    total_student = fields.Integer(string="Total Student", tracking=True, compute="_compute_total_student")
    available_student = fields.Integer(string="Available Student", tracking=True, compute="_compute_total_student")

    # Students & Subjects
    student_ids = fields.Many2many("student.student", string="Students", tracking=True, compute="_compute_student")
    subject_ids = fields.One2many("class.subject", "class_room_id", string="Subjects", tracking=True)

    @api.depends('academic_year_id', 'course_id')
    def _compute_student(self):
        """
        Compute students assigned to the class based on academic year, course, and class room
        """
        for rec in self:
            students = self.env['student.student'].search([
                ('academic_year_id', '=', rec.academic_year_id.id),
                ('course_id', '=', rec.course_id.id),
                ('class_room_id', '=', rec.id)
            ])
            rec.student_ids = students

    @api.depends('capacity', 'student_ids')
    def _compute_total_student(self):
        """
        Compute the total number of students and available seats
        """
        for rec in self:
            rec.total_student = len(rec.student_ids.ids)
            rec.available_student = rec.capacity - rec.total_student

    def assign_roll_no(self):
        """
        Assign sequential roll numbers to students in alphabetical order of their names
        """
        for rec in self:
            no = 1
            students = self.env['student.student'].search([('id', 'in', rec.student_ids.ids)], order="name ASC")
            for student in students:
                student.roll_no = no
                no += 1
