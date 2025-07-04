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


class WorkoutDays(models.Model):
    _name = "workout.days"
    _inherit = ['mail.thread']
    _description = "Workout Days"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(WorkoutDays, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list