# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    is_backorder = fields.Boolean("Is Backorder?", readonly=True)
    backorder_ref = fields.Char(string="Backorder Ref",compute='_get_backorder_details')
    demand_qty = fields.Float(string="Demand", readonly=True)

    def _get_backorder_details(self):
        for record in self:
            backorder_id = self.env['stock.picking'].search([('backorder_id','!=',False),('origin','=',record.name),('state','=','assigned')])
            if backorder_id:
                record.is_backorder = True
                record.backorder_ref = backorder_id.name
                record.demand_qty = sum(line.product_uom_qty for line in backorder_id.move_ids_without_package)
            else:
                record.is_backorder = False
                record.backorder_ref = None
                record.demand_qty = 0.0
