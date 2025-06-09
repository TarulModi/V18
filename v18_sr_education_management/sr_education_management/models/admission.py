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
from odoo.exceptions import ValidationError


class Admission(models.Model):

    _name = "admission.admission"
    _inherit = ['mail.thread']
    _description = "Admission"
    _rec_name = "name"

    name = fields.Char("Name", tracking=True)
    student_id = fields.Many2one("student.student", string="Student", tracking=True, copy=False)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    company_id = fields.Many2one("res.company", string="School", tracking=True, default=lambda self: self.env.company)
    admission_date = fields.Date(string="Admission Date", tracking=True)
    course_id = fields.Many2one("courses.courses", string="Course", tracking=True)

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
    student_achievement_ids = fields.One2many('student.achievement', 'admission_id', string="Student Achievement")
    is_alumni = fields.Boolean(string="Alumni", tracking=True)
    hobby_ids = fields.Many2many("hobby.hobby", "hobby_admission_rel", "hobby_id", "admission_id", string="Hobbies", tracking=True)
    state = fields.Selection([("draft", "Draft"),
                              ("confirm", "Confirm"),
                              ("doc_verification", "Docs Verification"),
                              ("enroll", "Enroll"),
                              ("cancel", "Cancel"),
                              ], string="State", tracking=True, default="draft")

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
    admission_number = fields.Char('Admission Number', readonly=True)
    enroll_no = fields.Char(related="student_id.enroll_no", string="Enrollment No")

    # Documents details
    documents_ids = fields.One2many("documents.documents", "admission_id", string="Documents")

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method to assign admission number from sequence
        """
        for vals in vals_list:
            vals['admission_number'] = self.env['ir.sequence'].next_by_code(
                'student.admission') or _("New")
        return super().create(vals_list)

    @api.onchange('student_id')
    def onchange_student_id(self):
        """
        Update admission name based on selected student
        """
        if self.student_id:
            self.name = self.student_id.name

    def verify_doc(self):
        # Filter out the documents that are not verified
        non_varify_doc = self.documents_ids.filtered(lambda doc: not doc.is_verified)
        # If all documents are verified, update the admission state to 'doc_verification'
        if not non_varify_doc:
            self.state = 'doc_verification'
        else:
            # Raise a validation error if there are unverified documents
            raise ValidationError(_("Please, Verify all documents."))

    def admission_confirm(self):
        """
        Confirm admission if documents are uploaded
        """
        if not self.documents_ids:
            raise ValidationError(_("Please set Documents."))
        self.state = 'confirm'

    def action_enroll(self):
        """
        Finalize enrollment:
        - Create student record
        - Link partner
        - Generate invoice from fees structure
        """
        # Prepare achievement lines
        # achievement_list = []
        # if self.student_achievement_ids:
        #     for achievement in self.student_achievement_ids:
        #         achievement_list.append((0, 0, {
        #             'name': achievement.name,
        #             'achievement_date': achievement.achievement_date,
        #             'description': achievement.description,
        #             'documents': achievement.documents
        #         }))
        # Get classroom with availability
        class_rooms = self.env['class.room'].search([
            ('academic_year_id', '=', self.academic_year_id.id),
            ('course_id', '=', self.course_id.id)
        ])
        class_room_ids = class_rooms.filtered(lambda c: c.available_student >= 1)
        if not class_room_ids:
            class_room_ids = class_rooms
        # Create student record
        student_id = self.env['student.student'].create({
            'name' : self.name,
            'student_image' : self.student_image,
            'gender' : self.gender,
            'bod' : self.bod,
            'street' : self.street,
            'street2' : self.street2,
            'zip' : self.zip,
            'city' : self.city,
            'state_id' : self.state_id.id,
            'country_id' : self.country_id.id,
            'emg_contact_person' : self.emg_contact_person,
            'emg_contact_person_no' : self.emg_contact_person_no,
            'email' : self.email,
            'mobile' : self.mobile,
            'mother_tongue_id' : self.mother_tongue_id.id,
            'blood_group' : self.blood_group,
            'nationality_id' : self.nationality_id.id,
            # 'student_achievement_ids' : achievement_list,
            'is_alumni' : self.is_alumni,
            'hobby_ids' : [(6, 0, self.hobby_ids.ids)],
            'father_name' : self.father_name,
            'father_mobile' : self.father_mobile,
            'father_occupation' : self.father_occupation,
            'mother_name' : self.mother_name,
            'mother_mobile' : self.mother_mobile,
            'mother_occupation' : self.mother_occupation,
            'school_name' : self.school_name,
            'registration_no' : self.registration_no,
            'pr_admission_date' : self.pr_admission_date,
            'pr_end_date' : self.pr_end_date,
            'course_id' : self.course_id.id,
            'academic_year_id': self.academic_year_id.id,
            'enroll_no' : self.env['ir.sequence'].next_by_code('student.enrollment'),
            'class_room_id' : class_room_ids.id or False
        })
        # Link admission to student
        if student_id:
            self.write({
                'student_id' : student_id.id,
                'state' : 'enroll',
            })
            for achievement in self.student_achievement_ids:
                achievement.student_id = student_id.id
            for doc in self.documents_ids:
                doc.student_id = student_id.id
            # Create partner record
            partner_id = self.env['res.partner'].create({
                'name': self.name,
                'email': self.email,
                'mobile': self.mobile,
                'street': self.street,
                'street2': self.street2,
                'zip': self.zip,
                'city': self.city,
                'state_id': self.state_id.id,
                'country_id': self.country_id.id,
                'student_id': student_id.id
            })
            student_id.partner_id = partner_id.id
            # Generate fee invoice
            fees_plan_id = self.env['fees.structure'].search([
                ('academic_year_id', '=', self.academic_year_id.id),
                ('term_ids', 'in', [self.academic_year_id.academic_terms_ids[0].id])
            ], limit=1)
            if fees_plan_id:
                lines = []
                for fees_line in fees_plan_id.line_ids:
                    lines.append((0, 0, {
                        'product_id': fees_line.product_id.id,
                        'price_unit': fees_line.amount
                    }))
                self.env['account.move'].create({
                    'partner_id': partner_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': lines
                })

    def action_cancel(self):
        """
        Cancel the admission
        """
        self.state = 'cancel'