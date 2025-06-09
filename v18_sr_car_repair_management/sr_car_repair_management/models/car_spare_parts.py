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
from odoo.exceptions import UserError, ValidationError


class CarSpareParts(models.Model):
    _name = "car.spare.parts"
    _description = "Car Spare Parts"
    _inherit = ['mail.thread']
    _rec_name = "product_id"

    diagnosis_id = fields.Many2one('car.diagnosis')
    checklist_id = fields.Many2one('car.repair.checklist', required=True, tracking=True, copy=False)
    product_id = fields.Many2one('product.product', required=True, tracking=True, copy=False)
    name = fields.Char('Name', required=True, tracking=True, copy=False)
    quantity = fields.Float("Quantity", default="1", tracking=True, copy=False)
    price = fields.Float("Price", tracking=True, copy=False)
    notes = fields.Text("Notes", copy=False, tracking=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.display_name
            self.price = self.product_id.list_price

    @api.onchange('quantity')
    def _onchange_quantity(self):
        if self.product_id:
            self.price = self.quantity * self.product_id.list_price
