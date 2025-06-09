# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class RepairEstimate(models.Model):
    _name = "repair.estimate"
    _description = "Repair Estimate"
    _inherit = ['mail.thread']
    _rec_name = "product_id"

    diagnosis_id = fields.Many2one('repair.diagnosis')
    checklist_id = fields.Many2one('repair.checklist', required=True, tracking=True, copy=False)
    product_id = fields.Many2one('product.product', required=True, copy=False)
    repair_work_order_id = fields.Many2one('repair.work.order', copy=False)
    vehicle_spare_parts_id = fields.Many2one('vehicle.spare.parts', copy=False)
    quantity = fields.Float("Quantity", default=1, copy=False)
    price = fields.Float("Price", copy=False)
    notes = fields.Text("Notes", copy=False)
    sub_total = fields.Float('Sub Total', compute="compute_sub_total", copy=False)
    is_service = fields.Boolean(string="Is Service", compute="_compute_is_service", store=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True, copy=False, tracking=True)

    @api.depends('product_id')
    def _compute_is_service(self):
        for rec in self:
            rec.is_service = rec.product_id.type == 'service' if rec.product_id else False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price

    @api.depends('quantity','price')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.quantity

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.vehicle_spare_parts_id:
                record.vehicle_spare_parts_id.repair_estimate_id = record.id
        return records

    def unlink(self):
        for record in self:
            if record.vehicle_spare_parts_id and not self.env.context.get('from_parts'):
                record.vehicle_spare_parts_id.with_context(from_estimate=True).unlink()
        return super().unlink()
