# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import datetime
from odoo import fields, api, models, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    rma_order_id = fields.Many2one("rma.order", copy=False, tracking=True)
    rma_count = fields.Integer(compute="compute_rma_count", tracking=True)
    rma_supplier_id = fields.Many2one("rma.supplier", copy=False, tracking=True)
    supplier_count = fields.Integer(compute="compute_supplier_count", tracking=True)

    @api.depends('rma_order_id')
    def compute_rma_count(self):
        for record in self:
            record.rma_count = self.env['rma.order'].search_count([('id', '=', record.rma_order_id.id)])

    @api.depends('rma_supplier_id')
    def compute_supplier_count(self):
        for record in self:
            record.supplier_count = self.env['rma.supplier'].search_count([('id', '=', record.rma_supplier_id.id)])

    def action_view_rma(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_customer_supplier_rma.action_rma_order")
        action['domain'] = [('id', '=', self.rma_order_id.id)]
        return action

    def action_view_rma_supplier(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_customer_supplier_rma.action_rma_supplier")
        action['domain'] = [('id', '=', self.rma_supplier_id.id)]
        return action

    def button_validate(self):
        result = super(StockPicking, self).button_validate()

        for record in self:
            if record.rma_order_id:
                record.rma_order_id.state = 'processing'

            if record.picking_type_id and record.picking_type_id.code == 'outgoing' and record.move_ids_without_package and record.rma_order_id:
                line_list = []
                for line in record.move_ids_without_package:
                    line_list.append((0, 0, {
                        'product_id' : line.product_id.id,
                        'quantity': line.quantity,
                    }))

                invoice_id = self.env['account.move'].create({
                    'partner_id': record.partner_id.id,
                    'invoice_date': datetime.datetime.today().date(),
                    'move_type': 'out_invoice',
                    'rma_order_id': record.rma_order_id.id,
                    'invoice_line_ids': line_list
                })
                if invoice_id:
                    invoice_id.action_post()
                    existing_invoices = record.rma_order_id.invoice_ids.ids or []
                    updated_invoice_ids = list(set(existing_invoices + [invoice_id.id]))
                    record.rma_order_id.invoice_ids = [(6, 0, updated_invoice_ids)]

            if record.picking_type_id and record.picking_type_id.code == 'incoming' and record.move_ids_without_package and record.rma_order_id:
                line_list = []
                for line in record.move_ids_without_package:
                    line_list.append((0, 0, {
                        'product_id' : line.product_id.id,
                        'quantity': line.quantity,
                    }))

                invoice_id = self.env['account.move'].create({
                    'partner_id': record.partner_id.id,
                    'invoice_date': datetime.datetime.today().date(),
                    'move_type': 'out_refund',
                    'rma_order_id': record.rma_order_id.id,
                    'invoice_line_ids': line_list
                })
                if invoice_id:
                    invoice_id.action_post()
                    existing_invoices = record.rma_order_id.invoice_ids.ids or []
                    updated_invoice_ids = list(set(existing_invoices + [invoice_id.id]))
                    record.rma_order_id.invoice_ids = [(6, 0, updated_invoice_ids)]

            if record.rma_supplier_id:
                record.rma_supplier_id.status = 'processing'

                if record.move_ids_without_package:
                    for move in record.move_ids_without_package:
                        if move.rma_supplied_line_id:
                            move.rma_supplied_line_id.received_qty = move.quantity