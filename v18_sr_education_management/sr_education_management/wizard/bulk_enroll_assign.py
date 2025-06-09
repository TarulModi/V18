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


class enrollAssign(models.TransientModel):
    _name = "bulk.enroll.assign"
    _description = "Assign Enrollment in bulk"

    academic_year_id = fields.Many2one("academic.year", string="Academic Year")
    course_id = fields.Many2one("courses.courses", string="Course")
    verified_admission_ids = fields.Many2many("admission.admission", "admission_enroll_rel", "enroll_id", "admission_id", string="Verified Admission")
    non_verified_admission_ids = fields.Many2many("admission.admission", "admission_nonenroll_rel", "nonenroll_id", "admission_id", string="Non Verified Admission")

    @api.onchange('academic_year_id', 'course_id')
    def _onchange_year_course(self):
        # When academic year and course are selected, fetch corresponding admissions by state
        if self.academic_year_id and self.course_id:
            # Admissions with verified documents (state = 'doc_verification')
            self.verified_admission_ids = self.env['admission.admission'].search([
                ('academic_year_id', '=', self.academic_year_id.id),
                ('course_id', '=', self.course_id.id),
                ('state', '=', 'doc_verification')
            ])
            # Admissions not yet verified (state = 'confirm')
            self.non_verified_admission_ids = self.env['admission.admission'].search([
                ('academic_year_id', '=', self.academic_year_id.id),
                ('course_id', '=', self.course_id.id),
                ('state', '=', 'confirm')
            ])

    def assign_enroll(self):
        # Ensure there are verified admissions before enrolling
        if not self.verified_admission_ids:
            raise ValidationError(_("There are no document-verified admissions to process. Please verify documents before proceeding with enrollment."))
        # Call the enrollment action on each verified admission
        for admission in self.verified_admission_ids:
            admission.action_enroll()