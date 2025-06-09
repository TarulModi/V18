# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from datetime import datetime
from odoo import models, fields, api, _


class HospitalIPDAdmission(models.Model):
    _name = 'hospital.ipd.admission'
    _description = 'Hospital IPD Admission'
    _order = 'admission_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Admission ID", readonly=True, copy=False, default="New", tracking=True)
    patient_id = fields.Many2one('res.partner', string="Patient", domain=[('is_patient', '=', True)], required=True, tracking=True)
    doctor_id = fields.Many2one('hr.employee', string="Assigned Doctor", domain=[('is_doctor', '=', True)], required=True, tracking=True)
    ward_id = fields.Many2one('hospital.ward', string="Ward", required=True, tracking=True)
    room_id = fields.Many2one('hospital.room', string="Room", required=True, domain="[('ward_id', '=', ward_id), ('is_available', '=', True)]", tracking=True)
    admission_date = fields.Datetime(string="Admission Date", required=True, default=fields.Datetime.now, tracking=True)
    discharge_date = fields.Datetime(string="Expected Discharge Date", tracking=True)
    state = fields.Selection([
        ('admitted', 'Admitted'),
        ('under_treatment', 'Under Treatment'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="admitted", tracking=True)
    treatment_notes = fields.Text(string="Treatment Notes", tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.ipd.admission') or "IPD00001"
        return super(HospitalIPDAdmission, self).create(vals)

    def action_under_treatment(self):
        self.state = 'under_treatment'

    def action_discharge(self):
        self.state = 'discharged'
        if self.room_id:
            self.room_id.is_available = True

    def action_cancel(self):
        self.state = 'cancelled'
        if self.room_id:
            self.room_id.is_available = True
