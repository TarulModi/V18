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


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    is_hospital = fields.Boolean(string="Is a Hospital", tracking=True)
    department_id = fields.Many2one('hr.department', string="Department", domain=[('is_hospital', '=', True)], store=True, tracking=True)
    department_doctor_ids = fields.Many2many(related="department_id.doctor_ids")
    doctor_ids = fields.Many2many('hr.employee', string="Doctors", required=True, tracking=True)
