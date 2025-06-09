# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from datetime import datetime, timedelta
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AcademicYear(models.Model):
    """
    Represents a full academic year (e.g., 2024–2025) within the education system.
    """
    _name = "academic.year"
    _inherit = ['mail.thread']
    _description = "Academic Year"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    term_structure_id = fields.Many2one("term.structure", string="Term Structure", tracking=True)
    start_date = fields.Date(string="Start Date", tracking=True)
    end_date = fields.Date(string="End Date", tracking=True)
    academic_terms_ids = fields.One2many("academic.terms", "academic_year_id")
    student_ids = fields.One2many('student.student', 'academic_year_id', 'Students')
    fees_structure_ids = fields.One2many('fees.structure', 'academic_year_id', 'Fees Structure')
    student_count = fields.Float('Student Count', compute="_compute_student_count")
    state = fields.Selection([("new", "New"),
                              ("open", "Open"),
                              ("close", "Close"),
                              ], string="State", tracking=True, default="new")
    invoice_ids = fields.Many2many('account.move', 'Invoice', compute="_compute_invoices")

    def _compute_invoices(self):
        for rec in self:
            rec.invoice_ids = self.env['account.move'].search([
                ('partner_id', 'in', self.student_ids.partner_id.ids),
                ('move_type', '=', 'out_invoice')
            ])


    def action_confirm(self):
        """
        Move academic year to 'open' state.
        Validates presence of terms before proceeding.
        """
        if not self.academic_terms_ids:
            raise ValidationError(_("Please, add academic Terms!"))
        self.state = "open"

    def action_close(self):
        """Set academic year to 'close' state."""
        self.state = "close"

    @api.depends('student_ids')
    def _compute_student_count(self):
        """Compute total students enrolled in the academic year."""
        for rec in self:
            rec.student_count = len(rec.student_ids.ids)

    def action_open_student(self):
        """
        Smart button: View related students for this academic year.
        Opens list or form view depending on count.
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

    def action_open_fees_structure(self):
        """
        Smart button: View fee structures linked to this academic year.
        """
        related_fees_structure = self.fees_structure_ids
        action = {
            'name': _("Related Fees Structure"),
            'type': 'ir.actions.act_window',
            'res_model': 'fees.structure',
            'view_mode': 'form',
        }
        if len(related_fees_structure) > 1:
            action['view_mode'] = 'list,form'
            action['domain'] = [('id', 'in', related_fees_structure.ids)]
            return action
        else:
            action['res_id'] = related_fees_structure.id
        return action

    def action_view_invoice(self):
        """
        Smart button: View invoices for all students in this academic year.
        Filters invoices by student partners.
        """
        action = self.env['ir.actions.actions']._for_xml_id('account.action_move_out_invoice_type')
        action['domain'] = [('partner_id', 'in', self.student_ids.partner_id.ids)]
        context = {
            'default_move_type': 'out_invoice',
        }
        action['context'] = context
        return action

    @api.constrains('start_date', 'end_date')
    def check_dates(self):
        """Ensure start_date is not after end_date."""
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError(_("End Date cannot be set before Start Date."))

    def generate_academic_terms(self):
        """
        Automatically generates academic terms based on the selected term structure.
        - Splits year duration into equal parts
        - Deletes any existing terms before regeneration
        """
        for record in self:
            if record.term_structure_id:
                term_count = record.term_structure_id.no_of_term
                start_date = fields.Date.from_string(record.start_date)
                end_date = fields.Date.from_string(record.end_date)

                # Delete existing academic terms
                record.academic_terms_ids.unlink()

                # Calculate the duration of each term
                term_duration = (end_date - start_date) // term_count

                # Generate academic terms and create records
                for i in range(term_count):
                    term_start_date = start_date + timedelta(days=i * term_duration.days)
                    term_end_date = term_start_date + timedelta(days=term_duration.days - 1)

                    # Create new academic term
                    self.env['academic.terms'].create({
                        'academic_year_id': record.id,
                        'name': f"Term {i + 1}",
                        'start_date': term_start_date,
                        'end_date': term_end_date,
                    })
