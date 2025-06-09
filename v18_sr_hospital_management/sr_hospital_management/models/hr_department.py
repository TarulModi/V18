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


class HospitalDepartment(models.Model):
    _inherit = 'hr.department'

    is_hospital = fields.Boolean(string="Is a Hospital", tracking=True)
    doctor_ids = fields.Many2many('hr.employee', string="Doctors", domain=[('is_doctor', '=', True)], tracking=True)
