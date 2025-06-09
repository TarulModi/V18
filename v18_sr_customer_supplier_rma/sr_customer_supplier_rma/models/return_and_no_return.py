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


class ReturnNoReturn(models.Model):
    _name = 'return.no.return'
    _inherit = ['mail.thread']
    _description = "Return/NoReturn"
    _rec_name = "name"

    name = fields.Char(string="RMA Reason", tracking=True, translate=True, required=True)
    reason_action = fields.Selection([
        ('refund_with_return_item', 'Replace with Returned Items'),
        ('refund_without_return_item', 'Replace without Returned Items'),
    ], tracking=True, required=True)