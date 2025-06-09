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


class HospitalBed(models.Model):
    _name = 'hospital.bed'
    _description = 'Hospital Bed'
    _rec_name = 'bed_no'
    _inherit = ['mail.thread']

    bed_no = fields.Char(string="Bed No.", required=True, tracking=True)
    ward_id = fields.Many2one('hospital.ward', string="Ward", ondelete='cascade', tracking=True)
    status = fields.Selection([
        ('occupied', 'Occupied'),
        ('unoccupied', 'UnOccupied'),
    ], string="Status", default="unoccupied", tracking=True)

    _sql_constraints = [
        ('uniq_bed_no', 'unique (bed_no)', 'A bed name must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_bed_no = f"{record.bed_no} (copy)"
            new_default = default.copy()
            new_default.update({'bed_no': new_bed_no})
            copied_vals = super(HospitalBed, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list
