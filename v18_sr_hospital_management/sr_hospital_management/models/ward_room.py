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


class HospitalWardRoom(models.Model):
    _name = 'hospital.ward.room'
    _description = 'Hospital Ward Room'
    _rec_name = 'room_id'
    _inherit = ['mail.thread']

    ward_id = fields.Many2one('hospital.ward', string="Ward", required=True, ondelete='cascade', tracking=True)
    room_id = fields.Many2one('hospital.room', string="Room", required=True, ondelete='cascade', tracking=True)
    room_type_id = fields.Many2one(related="room_id.room_type_id", string="Room Type", required=True, tracking=True)
    no_bed = fields.Integer(related="room_id.no_bed", string="Bed Count", required=True, tracking=True)
    per_bed_charges = fields.Float(related="room_type_id.per_bed_charges", string="Charges", tracking=True)
    room_bed_ids = fields.One2many(related="room_id.room_bed_ids")
    status = fields.Selection(related="room_id.status", string="Status", tracking=True, readonly=False, store=True)
    # is_available = fields.Boolean(string="Available", default=True, tracking=True)

    def unlink(self):
        for record in self:
            record.room_id.status = 'unoccupied'
        return super().unlink()
