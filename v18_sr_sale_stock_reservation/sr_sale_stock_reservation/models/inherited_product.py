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

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _compute_reservation(self):
        for product in self:
            reservation_ids = self.env['sale.order.line'].search([('product_id', '=', product.id), ('state', '=' , 'available')])
            product.quantity_reserve = sum([x.product_uom_qty for x in reservation_ids])
            product.reservation = len(reservation_ids)

    quantity_reserve = fields.Float(string='Reserved Quantity', compute="_compute_reservation")
    reservation = fields.Integer(string="Reserved", compute='_compute_reservation')
    