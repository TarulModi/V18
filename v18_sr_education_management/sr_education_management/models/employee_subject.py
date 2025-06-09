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


class EmployeeSubject(models.Model):
    _name = "employee.subject"
    _inherit = ['mail.thread']
    _description = "Employee Subject"
    _rec_name = "course_id"

    employee_id = fields.Many2one('hr.employee')
    course_id = fields.Many2one("courses.courses", tracking=True)
    subject_ids = fields.Many2many("subject.subject", "subject_employee_rel", "employee_id", "subject_id",
                                   string="Subjects")
