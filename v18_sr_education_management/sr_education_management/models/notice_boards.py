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


class NoticeBoards(models.Model):
    _name = "notice.boards"
    _inherit = ['mail.thread']
    _description = "Notice Boards"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    subject = fields.Char(string="Subject", tracking=True, translate=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    expiry_date = fields.Date(string="Expiry Date", tracking=True)
    description = fields.Text(string="Description", tracking=True)
    academic_year_id = fields.Many2one("academic.year", string="Academic Year", tracking=True)
    academic_terms_id = fields.Many2one("academic.terms", string="Academic Term", tracking=True)
    notice_boards_employee_ids = fields.One2many("notice.boards.employee", "notice_boards_id")
    courses_id = fields.Many2one("courses.courses", string="Course", tracking=True)
    subject_id = fields.Many2one("subject.subject", string="Subject", tracking=True)
    status = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('send_mail', 'Send Mail')], default="draft", copy=False)

    @api.constrains('start_date', 'expiry_date')
    def _check_date_range(self):
        """
        Ensure that the expiry date is not earlier than the start date.
        Raises a ValidationError if the condition is violated.
        """
        for record in self:
            if record.start_date and record.expiry_date:
                if record.expiry_date < record.start_date:
                    raise ValidationError("Expiry Date cannot be earlier than Start Date.")


    @api.onchange('courses_id')
    def _onchange_course_id(self):
        """
        When the course changes, update the related employees in the notice board.
        Finds employees teaching subjects in the selected course and adds them to the notice.
        """
        if self.courses_id:
            order_lines_data = [(5, 0)]
            employee_ids = self.env['hr.employee'].search([('subject_ids.course_id', '=', self.courses_id.id)])
            if employee_ids:
                for employee in employee_ids:
                    order_lines_data.append((0, 0, {
                        'employee_id': employee.id,
                    }))
                self.notice_boards_employee_ids = order_lines_data

    def button_confirm(self):
        """Change the status to 'confirm' when this button is clicked."""
        self.status = 'confirm'

    def send_mail(self):
        """
        Send email notifications for this notice board entry.
        Emails are sent to:
          - All employees linked to this notice board with a work email.
          - All students enrolled in the related course with a valid email.

        After sending the emails, the status is updated to 'send_mail'.
        """
        for record in self:
            email_to_list = []
            # Collect employees' emails
            for employee in record.notice_boards_employee_ids:
                if employee.employee_id.work_email:
                    email_to_list.append(employee.employee_id.work_email)
            # Collect students' emails enrolled in the course
            student_ids = self.env['student.student'].search([('course_id', '=', record.courses_id.id)])
            for student in student_ids:
                if student.email:
                    email_to_list.append(student.email)
            # Remove duplicates and empty emails
            email_to_list = list(filter(None, set(email_to_list)))

            if not email_to_list:
                # No recipients, skip sending
                continue

            mail_subject = f"Notice: {record.name}"
            mail_body = f"""
                <div>
                    <p><strong>Subject:</strong> {record.name}</p>
                    <p><strong>Description:</strong></p>
                    <p>{record.description or ''}</p>
                    <p><strong>Start Date:</strong> {record.start_date or 'N/A'}<br/>
                    <strong>Expiry Date:</strong> {record.expiry_date or 'N/A'}</p>
                    <br/>
                    <p><strong>Kind Regards,</strong><br/>{self.env.user.name}</p>
                </div>
            """
            # Create and send the email
            self.env['mail.mail'].create({
                'subject': mail_subject,
                'email_from': self.env.user.email or self.env.user.company_id.email,
                'email_to': ','.join(email_to_list),
                'body_html': mail_body,
            }).send()
            # Update status after sending emails
            record.status = 'send_mail'
