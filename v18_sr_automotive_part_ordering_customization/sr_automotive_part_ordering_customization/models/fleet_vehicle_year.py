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


class FleetVehicleYear(models.Model):
    _name = 'fleet.vehicle.year'
    _description = 'Vehicle Year'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    name = fields.Char("Name")
    start_year = fields.Integer("Start Year")
    end_year = fields.Integer("End Year")
