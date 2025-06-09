# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api


class Partner(models.Model):
    _inherit = "res.partner"
    
    credit_limit_custom = fields.Float('Credit Limit')
    credit_check = fields.Boolean('Check Credit')
    is_hold = fields.Boolean('Put on hold')
    blocking_limit = fields.Float(string="Blocking Limit")
