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


class RoomBed(models.Model):
    _name = 'room.bed'
    _description = 'Room Bed'
    _rec_name = 'room_id'
    _inherit = ['mail.thread']

    room_id = fields.Many2one('hospital.room', string="Room", required=True, ondelete='cascade', tracking=True)
    bed_id = fields.Many2one('hospital.bed', string="Bed", required=True, ondelete='cascade', tracking=True)
    status = fields.Selection(related="bed_id.status", string="Status", tracking=True, readonly=False, store=True)

    def unlink(self):
        for record in self:
            record.bed_id.status = 'unoccupied'
        return super().unlink()