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


class Courses(models.Model):
    _name = "courses.courses"
    _inherit = ['mail.thread']
    _description = "Courses"
    _rec_name = "name"

    # Basic course details
    name = fields.Char(string="Name", tracking=True, translate=True)
    code = fields.Char(string="Code", tracking=True, translate=True)
    course_image = fields.Binary("Course Image", tracking=True)
    parent_id = fields.Many2one("courses.courses", tracking=True)
    description = fields.Text("Description", tracking=True)

    # Relations
    courses_grade_ids = fields.One2many("courses.grade", "courses_id")
    courses_subject_ids = fields.One2many("subject.subject", "courses_id")
    admission_ids = fields.One2many('admission.admission', 'course_id', 'Admissions')
    student_ids = fields.One2many('student.student', 'course_id', 'Students')
    class_room_ids = fields.One2many('class.room', 'course_id', 'Class Rooms')
    timetable_ids = fields.One2many('school.timetable', 'course_id', 'Timetable')
    fees_structure_ids = fields.One2many('fees.structure', 'course_id', 'Fees Structure')
    invoice_ids = fields.Many2many('account.move', 'Invoice', compute="_compute_invoices")

    # Computed fields for quick counts
    admission_count = fields.Float('Admission Count', compute="_compute_addmission_count")
    student_count = fields.Float('Student Count', compute="_compute_student_count")

    # Faculty related to the course, computed from timetable days
    employee_ids = fields.Many2many("hr.employee", "Faculty", compute="compute_employee")

    def _compute_invoices(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([
                ('partner_id', 'in', self.student_ids.partner_id.ids),
                ('move_type', '=', 'out_invoice')
            ])

    def compute_employee(self):
        """Compute the employees (faculty) related to the course based on timetable days."""
        for rec in self:
            timetable_days = self.env['timetable.days'].search([('timetable_id.course_id', '=', rec.id)])
            rec.employee_ids = [(6, 0, timetable_days.employee_id.ids)]

    @api.depends('admission_ids')
    def _compute_addmission_count(self):
        """Compute the total number of admissions for each course."""
        for rec in self:
            rec.admission_count = len(rec.admission_ids.ids)

    @api.depends('student_ids')
    def _compute_student_count(self):
        """Compute the total number of students enrolled in each course."""
        for rec in self:
            rec.student_count = len(rec.student_ids.ids)

    def action_open_admission(self):
        """
        Open related admission records.
        If multiple admissions exist, show list and form views with domain filter.
        If only one admission, open form view directly.
        """
        related_admission = self.admission_ids
        action = {
            'name': _("Related Admissions"),
            'type': 'ir.actions.act_window',
            'res_model': 'admission.admission',
            'view_mode': 'form',
        }
        if len(related_admission) > 1:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', related_admission.ids)]
            return action
        else:
            action['res_id'] = related_admission.id
        return action

    def action_open_student(self):
        """
        Open related student records.
        Similar logic as action_open_admission: multiple opens list view, one opens form view.
        """
        related_student = self.student_ids
        action = {
            'name': _("Related Admissions"),
            'type': 'ir.actions.act_window',
            'res_model': 'student.student',
            'view_mode': 'form',
        }
        if len(related_student) > 1:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', related_student.ids)]
            return action
        else:
            action['res_id'] = related_student.id
        return action

    def action_open_class(self):
        """Open class rooms related to this course."""
        return {
            'name': _("Class Room"),
            'type': 'ir.actions.act_window',
            'res_model': 'class.room',
            'view_mode': 'list,form',
            'domain' : [('course_id', '=', self.id)],
            'context' : {'default_course_id': self.id},
        }

    def action_open_timetable(self):
        """Open timetable entries related to this course."""
        return {
            'name': _("Timetable"),
            'type': 'ir.actions.act_window',
            'res_model': 'school.timetable',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id},
        }

    def action_open_fees_structure(self):
        """Open fees structure records associated with this course."""
        return {
            'name': _("Fees Structure"),
            'type': 'ir.actions.act_window',
            'res_model': 'fees.structure',
            'view_mode': 'list,form',
            'domain': [('course_id', '=', self.id)],
            'context': {'default_course_id': self.id},
        }

    def action_view_invoice(self):
        """
        Open customer invoices related to students of this course.
        Filters invoices where partner_id matches any student's partner_id.
        """
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        action['domain'] = [('partner_id', 'in', self.student_ids.partner_id.ids)]
        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action
