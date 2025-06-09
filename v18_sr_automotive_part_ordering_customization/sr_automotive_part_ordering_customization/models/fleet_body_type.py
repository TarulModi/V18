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


class FleetBodyType(models.Model):
    _name = 'fleet.body.type'
    _description = 'Body Type'

    name = fields.Char("Name")
