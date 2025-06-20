# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import base64
import requests
from odoo import models, fields, _
from odoo.exceptions import UserError


class PushQtyToListingMirror(models.TransientModel):
    _name = "push.qty.to.listing.mirror"
    _description = "Push QTY Listing Mirror"

    sku = fields.Char('SKU(s)')

    # def push_qty_api_integration(self):
    #     vals = []
    #     for product in self.sku.split(','):
    #         product_id = self.env['product.product'].search([('default_code', '=', product)])
    #         if not product_id:
    #             raise UserError(_('Sku not found in system ' + product))
    #         loc_ids = self.env['stock.location'].search([('usage', '=', 'internal')])
    #         qty = 0
    #         for loc in loc_ids:
    #             if loc.name != 'Stock' and not loc.exclude_location:
    #                 qty += self.env['stock.quant']._get_available_quantity(product_id, loc)
    #         print("=======loc", qty)
    #         vals.append({
    #             "sku": product,
    #             "quantity": qty
    #         })
    #     payload = json.dumps(vals)
    #     headers = {
    #         'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE=',
    #         'Content-Type': 'application/json'
    #     }
    #     url = "https://api.listingmirror.com/api/v2/inventory/"
    #     response = requests.request("PUT", url, headers=headers, data=payload)
    #     response_json = response.json()
    #     print("======response_json", response_json)
    #     print("========not response_json.errors", not response_json.get('errors'))
    #     if not response_json.get('errors'):
    #         for record in vals:
    #             self.env['update.qty.log'].create({
    #                 'name': 'Manual QTY Pushed',
    #                 'origin': 'Manual QTY Pushed from Dashboard',
    #                 'qty': record.get('quantity'),
    #                 'pushed_qty': record.get('quantity'),
    #                 'product_id': self.env['product.product'].search([('default_code', '=', record.get('sku'))]).id,
    #             })
    #     else:
    #         raise UserError(_('Error From Listing mirror for push qty \n' + str(response_json.get('errors'))))


    def push_qty_api_integration(self):
        log_val = []
        product_list = []
        integration_name = "Manual QTY Pushed from Dashboard"
        for product in self.sku.split(','):
            product_id = self.env['product.product'].search([('default_code', '=', product)])
            if not product_id:
                # raise UserError(_('Sku not found in system ' + product))
                remark = f"Sku not found in system {product}"
                self.env['integration.error.log']._log_integration_error(product, integration_name, remark)
            product_list.append(product_id)

        if product_list:
            data_chunk = self.env['update.qty.log']._prepare_qty_data(product_list)
            self.env['update.qty.log']._push_qty_to_listing_mirror(data_chunk,
                                                                   integration_name="Inventory Adjustment Created")
            if data_chunk:
                for entry in data_chunk:
                    self.env['update.qty.log'].create({
                        'name': 'Manual QTY Pushed',
                        'origin': 'Manual QTY Pushed from Dashboard',
                        'qty': entry.get('quantity'),
                        'pushed_qty': entry.get('quantity'),
                        'product_id': entry.get('product_id'),
                    })
