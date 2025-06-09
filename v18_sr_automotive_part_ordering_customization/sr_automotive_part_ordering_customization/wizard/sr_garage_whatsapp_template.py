# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import io
import csv
import sys
import xlrd
import base64
import tempfile
import binascii
from odoo import models, fields, _
from odoo.exceptions import UserError, ValidationError


class GarageWPTemplate(models.TransientModel):
    _name = 'sr.garage.wp.template'
    _description = 'WhatsApp template for Garage'

    def _default_body(self):
        body_html = ""
        if self.env.context.get('active_id'):
            sale_id = self.env['sale.order'].browse(self.env.context.get('active_id'))
            if sale_id and (sale_id.vehicle_ids or sale_id.vehicle_model_id):
                vehicle_ids = sale_id.vehicle_ids
                if sale_id.vehicle_model_id:
                    vehicle_ids += self.env['fleet.vehicle'].search([('model_id', '=', sale_id.vehicle_model_id.id), ('id', 'not in', vehicle_ids.ids)])
                vehicle_list = []
                for vehicle in vehicle_ids:
                    vehicle_info = vehicle.display_name or ''
                    if vehicle.generation_id:
                        vehicle_info += ' - ' + vehicle.generation_id.name
                    if vehicle.fuel_type:
                        vehicle_info += ' - ' + dict(vehicle._fields['fuel_type'].selection).get(vehicle.fuel_type)
                    vehicle_list.append(vehicle_info)
                vehicle_list = list(set(vehicle_list))
                body_html += "<b>"
                for vehicle_data in vehicle_list:
                    body_html += vehicle_data + "<br/>"
                body_html += "</b>"

            if sale_id and sale_id.order_line:
                count = 0
                for line in sale_id.order_line:
                    count += 1
                    body_html += str(count) + " . " + line.product_id.display_name + " - " + str(line.product_uom_qty) + " Pc - Rs <b>" + str(line.price_unit) + "/-</b>"
                    body_html += "<br/>"
                body_html += "Invoice Amount : <b>" + str(sale_id.amount_total) + "/-</b>"
        return body_html

    body = fields.Html('Body', default=_default_body)
