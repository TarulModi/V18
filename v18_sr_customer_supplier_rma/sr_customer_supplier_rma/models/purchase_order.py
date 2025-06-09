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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    rma_supplier_id = fields.Many2one("rma.supplier", copy=False, tracking=True)
    rma_supplier_count = fields.Integer(compute="compute_rma_supplier_count", tracking=True)

    @api.depends('rma_supplier_id')
    def compute_rma_supplier_count(self):
        for record in self:
            record.rma_supplier_count = self.env['rma.supplier'].search_count([('id', '=', record.rma_supplier_id.id)])

    def action_view_rma(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_customer_supplier_rma.action_rma_supplier")
        action['domain'] = [('id', '=', self.rma_supplier_id.id)]
        return action