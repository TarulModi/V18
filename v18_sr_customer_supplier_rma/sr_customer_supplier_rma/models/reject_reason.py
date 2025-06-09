# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, api, models, _


class RejectReason(models.Model):
    _name = 'reject.reason'
    _inherit = ['mail.thread']
    _description = "Reject Reason"
    _rec_name = "name"

    name = fields.Char(string="Reject Reason", tracking=True, translate=True, required=True)
    is_reject_reason = fields.Boolean("Is Customer Reject Reason")
    active = fields.Boolean("Active", default=True)
