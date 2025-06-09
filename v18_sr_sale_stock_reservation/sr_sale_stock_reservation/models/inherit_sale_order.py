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
import datetime      

class SalesOrder(models.Model):
    _inherit = 'sale.order'

    sale_type = fields.Selection([('reservation', 'Reservation'), ('quotation', 'Quotation')], default="quotation", string='Type')
    state = fields.Selection(selection_add=[('waiting', 'Waiting Availability'), ('available', 'Available')])


    @api.model
    def create(self, vals):
        order_id = super(SalesOrder, self).create(vals)
        ICPSudo = self.env['ir.config_parameter'].sudo()
        reservation_expiry_days = ICPSudo.get_param('reservation_expiry_days') or 15
        order_id.validity_date = (fields.Date.from_string(order_id.date_order)) + datetime.timedelta(days=int(reservation_expiry_days))
        if order_id.order_line:
            for line in order_id.order_line:
                if line.product_id.type == 'product':
                    if line.product_uom_qty > line.available_quantity:
                        order_id.state = 'waiting'
                        return order_id
            order_id.state = 'available'
        else:
            order_id.state = 'draft'
        return order_id

    @api.model
    def write(self, vals):
        super(SalesOrder, self).write(vals)
        if vals.get('order_line'):
            if self.order_line:
                for line in self.order_line:
                    if line.product_id.type == 'product':
                        if line.product_uom_qty > line.available_quantity:
                            self.state = 'waiting'
                            return True
                self.state = 'available'
            else:
                self.state = 'draft'
        return True

    def button_force_available(self):
        for record in self:
            record.state = 'waiting'
        return True


    @api.model
    def _find_expired_reservation(self):
        reservation = self.search([('state', 'in', ['waiting', 'available']), ('sale_type', '=', 'reservation')])
        for record in reservation:
            if (fields.Date.from_string(record.validity_date)) < datetime.datetime.today().date():
                record.action_cancel()

class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    def _compute_onchange_quantity(self):
        for line in self:
            if line.product_id.type == 'product':
                line.available_quantity = line.product_id.qty_available - line.product_id.quantity_reserve
                
        return
     
    available_quantity = fields.Float('Available Quantity', compute = '_compute_onchange_quantity')

