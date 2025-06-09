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


class SaleCancelReason(models.Model):
    _name = 'sale.cancel.reason'
    _description = 'Sale Order Cancel Reason'

    name = fields.Char("Name")
