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


class ProductModelCode(models.Model):
    _name = 'product.model.code'
    _description = 'Product Model Code'

    product_id = fields.Many2one('product.product')
    product_tmpl_id = fields.Many2one('product.template')
    fleet_vehicle_id = fields.Many2one('fleet.vehicle', "Model")
    model_year = fields.Char(related="fleet_vehicle_id.model_year", string="Make Year")
    fleet_variant_id = fields.Many2one('fleet.variant', related="fleet_vehicle_id.fleet_variant_id", string='Variant')
    fuel_type = fields.Selection(related="fleet_vehicle_id.fuel_type")
    transmission = fields.Selection(related="fleet_vehicle_id.transmission")
    generation_id = fields.Many2one('fleet.generation', related="fleet_vehicle_id.generation_id")
    code = fields.Char("OEM SKU Code")
    brand_id = fields.Many2one('product.brand', "Brand")
