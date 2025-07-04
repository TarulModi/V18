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


class gymMemberMembership(models.Model):
    _name = "gym.member.membership"
    _inherit = ['mail.thread']
    _description = "GYM Member Membership"
    _rec_name = "membership_id"

    # name = fields.Char(string="Name", tracking=True, translate=True)
    membership_id = fields.Many2one('gym.membership', string="Membership", tracking=True)
    start_date = fields.Date("Start Date", tracking=True)
    end_date = fields.Date("End Date", tracking=True)
    fees = fields.Float("Fees", tracking=True)
    partner_id = fields.Many2one("res.partner")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('paid', 'Confirm With Paid'),
        ('cancel', 'Cancel')],
        default='draft')