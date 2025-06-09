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


class HospitalPatient(models.Model):
    _inherit = "res.partner"

    is_patient = fields.Boolean(string="Is a Patient", tracking=True)
    patient_id = fields.Char(string="Patient ID", readonly=True, copy=False, tracking=True)
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", tracking=True)
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B-'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-')
    ], string="Blood Type", tracking=True)
    medical_history = fields.Text(string="Medical History", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('is_patient', False) and not vals.get('patient_id'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('res.partner') or 'NEW'
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if 'is_patient' in vals and vals['is_patient'] and not self.patient_id:
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('res.partner') or 'NEW'
        return super(HospitalPatient, self).write(vals)