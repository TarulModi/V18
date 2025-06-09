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


class Student(models.Model):
    _name = "student.student"
    _inherit = ['mail.thread']
    _description = "Student"
    _rec_name = "name"

    #Student profile
    name = fields.Char(string="Name", tracking=True, translate=True)
    student_image = fields.Binary("Student Image", tracking=True)
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender",
                              tracking=True, default="male")
    bod = fields.Date(string="Birth Date", tracking=True)
    street = fields.Char('Street', readonly=False, store=True, tracking=True, translate=True)
    street2 = fields.Char('Street2', readonly=False, store=True, tracking=True, translate=True)
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True, tracking=True, translate=True)
    city = fields.Char('City', readonly=False, store=True, tracking=True, translate=True)
    state_id = fields.Many2one("res.country.state", string='State', readonly=False, store=True,
                               domain="[('country_id', '=?', country_id)]", tracking=True)
    country_id = fields.Many2one('res.country', string='Country', readonly=False, store=True, tracking=True)
    emg_contact_person = fields.Char(string="Emergency Contact Person", tracking=True, translate=True)
    emg_contact_person_no = fields.Char(string="Emergency Contact Person Number", tracking=True, translate=True)
    email = fields.Char(string="Email", tracking=True, translate=True)
    mobile = fields.Char(string="Mobile", tracking=True, translate=True)
    mother_tongue_id = fields.Many2one("mother.tongue", string="Mother Tongue", tracking=True)
    blood_group = fields.Selection([("a+", "A+"),
                                    ("b+", "B+"),
                                    ("o+", "O+"),
                                    ("ab+", "AB+"),
                                    ("a-", "A-"),
                                    ("b-", "B-"),
                                    ("o-", "O-"),
                                    ("ab-", "AB-"),
                                    ], string="Blood Group", tracking=True, default="a+")
    nationality_id = fields.Many2one('res.country', string='Nationality', tracking=True)
    student_achievement_ids = fields.One2many('student.achievement', 'student_id', string="Student Achievement")
    is_alumni = fields.Boolean(string="Alumni", tracking=True)
    hobby_ids = fields.Many2many("hobby.hobby", "hobby_student_rel", "hobby_id", "student_id", string="Hobbies",
                                 tracking=True)
    course_id = fields.Many2one("courses.courses", string="Course", tracking=True)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    enroll_no = fields.Char(string="Enrollment No", readonly=True)
    roll_no = fields.Integer(string="Roll No", tracking=True)
    class_room_id = fields.Many2one("class.room", string="Class Room", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Partner")

    # Parents Details
    father_name = fields.Char(string="Name", tracking=True, translate=True)
    father_mobile = fields.Char(string="Mobile", tracking=True, translate=True)
    father_occupation = fields.Char(string="Occupation", tracking=True, translate=True)

    mother_name = fields.Char(string="Name", tracking=True, translate=True)
    mother_mobile = fields.Char(string="Mobile", tracking=True, translate=True)
    mother_occupation = fields.Char(string="Occupation", tracking=True, translate=True)

    # Previous school details
    school_name = fields.Char("School Name", tracking=True)
    registration_no = fields.Char("Registration No.", tracking=True)
    pr_admission_date = fields.Date(string="Admission Date", tracking=True)
    pr_end_date = fields.Date(string="End Date", tracking=True)

    invoice_ids = fields.Many2many('account.move', 'Invoice', compute="_compute_invoices")
    documents_ids = fields.One2many("documents.documents", "student_id", string="Documents")

    def _compute_invoices(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([
                ('partner_id', 'in', self.partner_id.ids),
                ('move_type', '=', 'out_invoice')
            ])

    def action_view_invoice(self):
        """
        Opens the customer invoices related to this student.
        Uses the linked partner_id to filter invoices.
        """
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        action['domain'] = [('partner_id', 'in', self.partner_id.ids)]
        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action
