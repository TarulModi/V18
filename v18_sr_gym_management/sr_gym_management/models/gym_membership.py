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


class gymMembership(models.Model):
    _name = "gym.membership"
    _inherit = ['mail.thread']
    _description = "GYM Membership"
    _rec_name = "name"

    name = fields.Char(string="Name", tracking=True, translate=True)
    start_date = fields.Date("Start Date", tracking=True)
    end_date = fields.Date("End Date", tracking=True)
    fees = fields.Float("Fees", tracking=True)
    partner_ids = fields.Many2many("res.partner", string="Members", tracking=True)

    def copy_data(self, default=None):
        vals_list = []
        default = default or {}
        for record in self:
            new_name = f"{record.name} (copy)"
            new_default = default.copy()
            new_default.update({'name': new_name})
            copied_vals = super(gymMembership, record).copy_data(default=new_default)
            vals_list.extend(copied_vals)
        return vals_list