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


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    _rec_name = "import_display_name"

    vehicle_year_ids = fields.One2many('fleet.vehicle.year', 'vehicle_id', 'Vehicle Year')
    generation_id = fields.Many2one('fleet.generation')
    type_id = fields.Many2one('fleet.type')
    body_type_id = fields.Many2one('fleet.body.type')
    fleet_variant_id = fields.Many2one('fleet.variant', 'Variant')
    import_display_name = fields.Char("Display Name")
    fuel_type = fields.Selection(selection_add=[
        ('petrol', 'Petrol'),
    ], ondelete={'petrol': 'cascade'})
