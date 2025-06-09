# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, _


class SupplierReason(models.Model):
    _name = 'rma.supplier.reason'
    _description = 'RMA Supplier Reason'
    _inherit = ['mail.thread']
    _rec_name = 'rma_reason'

    rma_reason = fields.Char(string='RMA Reason', tracking=True, required= True)
    reason_action = fields.Selection(
        [('replace', 'Replace'), ('refund', 'Refund'), ('repair', 'Repair')],
        string='Reason Action',
        tracking=True,
        default="replace"
    )
