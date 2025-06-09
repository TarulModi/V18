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


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    picking_type_id = fields.Many2one(related="company_id.picking_type_id", readonly=False)
    without_picking_type_id = fields.Many2one(related="company_id.without_picking_type_id", readonly=False)
    stock_route_id = fields.Many2one(related="company_id.stock_route_id", readonly=False)
    rma_source_picking_type_id = fields.Many2one(related="company_id.rma_source_picking_type_id", readonly=False)
    rma_destination_picking_type_id = fields.Many2one(related="company_id.rma_destination_picking_type_id", readonly=False)
