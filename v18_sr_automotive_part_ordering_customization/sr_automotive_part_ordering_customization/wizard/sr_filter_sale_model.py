# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.osv import expression
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

FUEL_TYPES = [
    ('diesel', 'Diesel'),
    ('gasoline', 'Gasoline'),
    ('full_hybrid', 'Full Hybrid'),
    ('plug_in_hybrid_diesel', 'Plug-in Hybrid Diesel'),
    ('plug_in_hybrid_gasoline', 'Plug-in Hybrid Gasoline'),
    ('cng', 'CNG'),
    ('lpg', 'LPG'),
    ('hydrogen', 'Hydrogen'),
    ('electric', 'Electric'),
    ('petrol', 'Petrol'),
]


class srFilterSaleVehicleModel(models.TransientModel):
    _name = 'sr.filter.sale.vehicle.model'
    _description = 'Filter Sale Vehicle Model'

    model_year = fields.Char("Model Year")
    model_id = fields.Many2one("fleet.vehicle.model", "Model Name")
    fleet_variant_id = fields.Many2one("fleet.variant", string='Variant')
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', store=True, readonly=False)
    transmission = fields.Selection(
        [('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission',store=True)
    generation_id = fields.Many2one('fleet.generation')
    model_line_ids = fields.One2many("sr.filter.sale.vehicle.model.line", "filter_sale_model_id")

    @api.onchange('model_year','model_id','fleet_variant_id','fuel_type','transmission','generation_id',)
    def _onchange_product_suppliers(self):
        model_line_vals = [(5, 0, 0)]
        combine =  expression.AND
        domains = []
        domain = []
        for rec in self:
            if rec.model_year:
                domains.append([('model_year', '=', rec.model_year)])
            if rec.model_id:
                domains.append([('model_id', '=', rec.model_id.id)])
            if rec.fleet_variant_id:
                domains.append([('fleet_variant_id', '=', rec.fleet_variant_id.id)])
            if rec.fuel_type:
                domains.append([('fuel_type', '=', rec.fuel_type)])
            if rec.transmission:
                domains.append([('transmission', '=', rec.transmission)])
            if rec.generation_id:
                domains.append([('generation_id', '=', rec.generation_id.id)])
            domain = combine(domains)
        fleet_vehicle_ids = self.env['fleet.vehicle'].search(domain)
        if fleet_vehicle_ids and (self.model_year or self.model_id or self.fleet_variant_id or self.fuel_type or self.transmission or self.generation_id):
            for fleet_vehicle in fleet_vehicle_ids:
                vals = {
                    'vehicle_id': fleet_vehicle.id,
                    'model_year': fleet_vehicle.model_year,
                    'fleet_variant_id': fleet_vehicle.fleet_variant_id.id,
                    'fuel_type': fleet_vehicle.fuel_type,
                    'transmission': fleet_vehicle.transmission,
                    'generation_id': fleet_vehicle.generation_id.id,
                }
                model_line_vals.append((0, 0, vals))
        self.model_line_ids = model_line_vals


    def filter_vehicle_model_data(self):
        model_line_ids = self.model_line_ids.filtered(lambda l: l.is_select)
        vehicle_list = []
        if not model_line_ids:
            raise ValidationError("Select Atleast one model")
        else:
            active_id = self.env.context.get('active_id')
            sale_order = self.env['sale.order'].browse(active_id)
            for record in model_line_ids:
                vehicle_list.append(record.vehicle_id.id)
            if sale_order:
                sale_order.vehicle_ids = [(6, 0, vehicle_list)]


class srFilterSaleVehicleModeLinel(models.TransientModel):
    _name = 'sr.filter.sale.vehicle.model.line'
    _description = 'Filter Sale Vehicle Model Line'

    filter_sale_model_id = fields.Many2one('sr.filter.sale.vehicle.model')
    is_select = fields.Boolean("Select")
    vehicle_id = fields.Many2one("fleet.vehicle", string="Model")

    model_year = fields.Char("Model Year")
    fleet_variant_id = fields.Many2one('fleet.variant', 'Variant')
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', store=True, readonly=False)
    transmission = fields.Selection(
        [('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', store=True)
    generation_id = fields.Many2one('fleet.generation')
