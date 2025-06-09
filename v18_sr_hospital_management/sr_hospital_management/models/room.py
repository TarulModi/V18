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
from odoo.exceptions import ValidationError


class HospitalRoom(models.Model):
    _name = 'hospital.room'
    _description = 'Hospital Room'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Room Number", required=True, tracking=True)
    ward_id = fields.Many2one('hospital.ward', string="Ward", ondelete='cascade', tracking=True)
    room_type_id = fields.Many2one('room.type', string="Room Type", required=True, tracking=True)
    no_bed = fields.Integer(related="room_type_id.no_bed", required=True, tracking=True)
    per_bed_charges = fields.Float(related="room_type_id.per_bed_charges", string="Charges", tracking=True)
    is_available = fields.Boolean(string="Available", default=True, tracking=True)
    room_bed_ids = fields.One2many("room.bed", "room_id", string="Bed Details", tracking=True)
    status = fields.Selection([
        ('occupied', 'Occupied'),
        ('unoccupied', 'UnOccupied'),
    ], string="Status", default="unoccupied", tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique (name)', 'A room name must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(HospitalRoom, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list

    @api.constrains('room_bed_ids')
    def _check_bed_limit(self):
        for record in self:
            if len(record.room_bed_ids) > record.no_bed:
                raise ValidationError(
                    f"Number of beds assigned ({len(record.room_bed_ids)}) exceeds the allowed limit ({record.no_bed}) for room {record.name}.")
            if record.room_bed_ids:
                for bed in record.room_bed_ids:
                    bed.status = 'occupied'
