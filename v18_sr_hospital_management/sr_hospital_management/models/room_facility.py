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


class RoomFacility(models.Model):
    _name = 'room.facility'
    _description = 'Room Facility'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name", required=True, tracking=True)

    _sql_constraints = [
        ('uniq_name', 'unique (name)', 'A facility name must be unique.'),
    ]

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(RoomFacility, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list
