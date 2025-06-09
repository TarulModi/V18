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


class HospitalSpecialization(models.Model):
    _name = 'hospital.specialization'
    _description = 'Doctor Specialization'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Specialization", required=True, tracking=True)
    is_medical = fields.Boolean(string="Is Medical Specialization", default=True, tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique (name)', 'A specialization name must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(HospitalSpecialization, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list
