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


class SalesOrder(models.Model):
    _inherit = 'sale.order'

    rma_order_id = fields.Many2one("rma.order", copy=False, tracking=True)
    rma_count = fields.Integer(compute="compute_rma_count", tracking=True)

    @api.depends('rma_order_id')
    def compute_rma_count(self):
        for record in self:
            record.rma_count = self.env['rma.order'].search_count([('id', '=', record.rma_order_id.id)])

    def action_view_rma(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_customer_supplier_rma.action_rma_order")
        action['domain'] = [('id', '=', self.rma_order_id.id)]
        return action