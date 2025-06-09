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


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment'
    _order = 'appointment_date desc'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Appointment ID", readonly=True, copy=False, default="New", tracking=True)
    patient_id = fields.Many2one('res.partner', string="Patient", domain=[('is_patient', '=', True)], required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string="Department", store=True, domain=[('is_hospital', '=', True)], tracking=True)
    doctor_ids = fields.Many2many(related="department_id.doctor_ids")
    doctor_id = fields.Many2one('hr.employee', string="Doctor", required=True, tracking=True)
    appointment_date = fields.Datetime(string="Appointment Date", required=True, default=fields.Datetime.now, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="draft", tracking=True)
    notes = fields.Text(string="Appointment Notes", tracking=True)


    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or "APT00001"
        return super(HospitalAppointment, self).create(vals)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_complete(self):
        self.state = 'completed'

    def action_cancel(self):
        self.state = 'cancelled'
