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


class PurchaseCancelReason(models.Model):
    _name = 'purchase.cancel.reason'
    _description = 'Purchase Order Cancel Reason'

    name = fields.Char("Name")
