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


class VendorWPTemplate(models.TransientModel):
    _name = 'sr.vendor.wp.template'
    _description = 'WhatsApp template for Supplier'

    def _default_body(self):
        body_html = ""
        if self.env.context.get('active_id'):
            po_id = self.env['purchase.order'].browse(self.env.context.get('active_id'))
            if po_id.order_line.sale_order_line_id and po_id.order_line.sale_order_line_id.order_id:
                sale_id = po_id.order_line.sale_order_line_id.order_id
                vehicle_ids = sale_id.vehicle_ids
                if sale_id.vehicle_model_id:
                    vehicle_ids += self.env['fleet.vehicle'].search(
                        [('model_id', '=', sale_id.vehicle_model_id.id), ('id', 'not in', vehicle_ids.ids)])
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

            if po_id and po_id.order_line:
                count = 0
                for line in po_id.order_line:
                    count += 1
                    body_html += str(count) + " . " + line.product_id.display_name + " -- " + str(line.product_uom_qty) + " Pc"
                    body_html += "<br/>"
        return body_html

    body = fields.Html('Body', default=_default_body)
