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
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class VehicleSpareParts(models.Model):
    _name = "vehicle.spare.parts"
    _description = "Vehicle Spare Parts"
    _inherit = ['mail.thread']
    _rec_name = "product_id"

    diagnosis_id = fields.Many2one('repair.diagnosis')
    product_id = fields.Many2one('product.product', required=True, tracking=True, copy=False)
    quantity = fields.Float("Quantity", default=1, tracking=True, copy=False)
    price = fields.Float("Price", tracking=True, copy=False)
    notes = fields.Text("Notes", copy=False, tracking=True)
    sub_total = fields.Float('Sub Total', compute="compute_sub_total", copy=False)
    repair_work_order_id = fields.Many2one('repair.work.order', copy=False)
    repair_estimate_id = fields.Many2one('repair.estimate', copy=False)
    is_service = fields.Boolean(string='Is Service', compute='_compute_is_service', store=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True, copy=False, tracking=True)

    @api.depends('product_id')
    def _compute_is_service(self):
        for rec in self:
            rec.is_service = rec.product_id.type == 'service'

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.price = self.product_id.list_price

    @api.depends('quantity', 'price')
    def compute_sub_total(self):
        for record in self:
            record.sub_total = record.price * record.quantity

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if record.repair_work_order_id and not record.repair_estimate_id:
                work_order = record.repair_work_order_id
                checklist = work_order.checklist_id
                diagnosis = work_order.diagnosis_id

                if checklist and diagnosis:
                    estimate = self.env['repair.estimate'].create({
                        'diagnosis_id': diagnosis.id,
                        'checklist_id': checklist.id,
                        'product_id': record.product_id.id,
                        'quantity': record.quantity,
                        'price': record.price,
                        'notes': record.notes,
                        'repair_work_order_id': work_order.id,
                        'vehicle_spare_parts_id': record.id,
                    })
                    record.repair_estimate_id = estimate.id
        return records

    def unlink(self):
        for record in self:
            _logger.info("Trying to unlink: %s", record)
            if record.repair_estimate_id and not self.env.context.get('from_estimate'):
                _logger.info("Unlinking linked repair_estimate_id: %s", record.repair_estimate_id.id)
                record.repair_estimate_id.with_context(from_parts=True).sudo().unlink()
        return super().unlink()