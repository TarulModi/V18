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


class ResCompany(models.Model):
    _inherit = "res.company"

    period = fields.Integer(
        "Warranty Expire Notification", store=True, default=1)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    period = fields.Integer(
        "Warranty Expire Notification", related="company_id.period", readonly=False
    )
