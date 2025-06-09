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


class HospitalWard(models.Model):
    _name = 'hospital.ward'
    _description = 'Hospital Ward'
    _rec_name = 'name'
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Ward Name", required=True, tracking=True)
    ward_code = fields.Char(string="Ward Code", required=True, unique=True, tracking=True)
    # capacity = fields.Integer(string="Total Capacity", required=True, tracking=True)
    room_ids = fields.One2many('hospital.ward.room', 'ward_id', string="Rooms", tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique (name)', 'A ward name must be unique.'),
        ('uniq_ward_code', 'unique (ward_code)', 'A ward code must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_code = f"{record.ward_code} (copy)"
            new_default = default.copy()
            new_default.update({
                'name': new_name,
                'ward_code': new_code,
            })
            copied_vals = super(HospitalWard, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list

    @api.constrains('room_ids')
    def _check_bed_limit(self):
        for record in self:
            if record.room_ids:
                for room_id in record.room_ids:
                    room_id.status = 'occupied'
