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


class company(models.Model):
    _inherit = 'res.company'

    picking_type_id = fields.Many2one('stock.picking.type', string="Source Picking Type")
    without_picking_type_id = fields.Many2one('stock.picking.type', string="Without Return Items Picking Type")
    stock_route_id = fields.Many2one('stock.route', string="RMA Route for SO")
    rma_source_picking_type_id = fields.Many2one('stock.picking.type', string="Source Picking Type")
    rma_destination_picking_type_id = fields.Many2one('stock.picking.type', string="Destination Picking Type")
