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


class RoomType(models.Model):
    _name = 'room.type'
    _description = 'Room Type'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", required=True, tracking=True)
    per_bed_charges = fields.Float(string="Charges", tracking=True)
    no_bed = fields.Integer(string="No of Beds")
    room_facility_ids = fields.Many2many("room.facility", "room_facility_type_rel", "room_facility_id", "type_id", string="Facilities")

    _sql_constraints = [
        ('uniq_name', 'unique (name)', 'A room type name must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(RoomType, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list