# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import json
import base64
import requests
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    asin = fields.Char('ASIN')
    upc = fields.Char('UPC')
    mpn = fields.Char('MPN')
    brand = fields.Char('Brand')

    # def action_cron_push_qty_api(self):
    #     available_qty_by_product = {}
    #     quants = self.env['stock.quant'].search(
    #         [('location_id.usage', '=', 'internal'), ('location_id.exclude_location', '=', False),
    #          ('location_id.name', '!=', 'Stock')])
    #     for quant in quants:
    #         available_qty_by_product.setdefault(quant.product_id.id, 0)
    #         available_qty_by_product[quant.product_id.id] += quant.available_quantity
    #     chunk_size = 100
    #     vals = []
    #     segregated_data = []
    #     for i in range(0, len(self.search([])), chunk_size):
    #         product_chunk = self.search([])[i:i + chunk_size]
    #         data_chunk = []
    #         for product in product_chunk:
    #             data_chunk.append({
    #                 "sku": product.default_code,
    #                 "quantity": available_qty_by_product.get(product.id, 0)
    #             })
    #         segregated_data.append(data_chunk)
    #     integration_name = 'Push QTY API Integrations with Listing Mirror'
    #     date = fields.Datetime.now()
    #     for a in segregated_data:
    #         payload = json.dumps(a)
    #         # headers = {
    #         #     'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE=',
    #         #     'Content-Type': 'application/json'
    #         # }
    #         # url = "https://api.listingmirror.com/api/v2/inventory/"
    #         # response = requests.request("PUT", url, headers=headers, data=payload)
    #         # response_json = response.json()
    #         print("=========aaaaaaaaaaa=========", a)
    #         print("=========response_json=========", response_json)

    # def action_cron_push_qty_api(self):
    #     # config = self.env['ir.config_parameter'].sudo()
    #     # kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
    #     # kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')
    #     #
    #     # if not kwik_url or not kwik_token:
    #     #     raise UserError(_("API URL or Token is not configured."))
    #     #
    #     # headers = {
    #     #     'Authorization': f"Basic {kwik_token}",
    #     #     'Content-Type': 'application/json'
    #     # }
    #     # url = f"{kwik_url}inventory/"
    #
    #     available_qty_by_product = {}
    #     quants = self.env['stock.quant'].search([
    #         ('location_id.usage', '=', 'internal'),
    #         ('location_id.exclude_location', '=', False),
    #         ('location_id.name', '!=', 'Stock')
    #     ])
    #     for quant in quants:
    #         available_qty_by_product.setdefault(quant.product_id.id, 0)
    #         available_qty_by_product[quant.product_id.id] += quant.available_quantity
    #
    #     # Process products in chunks
    #     chunk_size = 100
    #     all_products = self.search([])
    #     for i in range(0, len(all_products), chunk_size):
    #         product_chunk = all_products[i:i + chunk_size]
    #         data_chunk = []
    #         for product in product_chunk:
    #             data_chunk.append({
    #                 "sku": product.default_code if product.default_code else product.name,
    #                 "quantity": available_qty_by_product.get(product.id, 0)
    #             })
    #
    #         # Create log records for this chunk
    #         integration_name = 'Push QTY API Integrations with Listing Mirror'
    #         date = fields.Datetime.now()
    #         print("---data_chunk------------", data_chunk)
    #         for entry in data_chunk:
    #             print("---entry------------",entry)
    #             payload = json.dumps(entry)
    #             # response = requests.request("PUT", url, headers=headers, data=payload)
    #             # response_json = response.json()


    def action_cron_push_qty_api(self):
        all_products = self.search([])
        chunk_size = 100
        for i in range(0, len(all_products), chunk_size):
            product_chunk = all_products[i:i + chunk_size]
            data_chunk = self.env['update.qty.log']._prepare_qty_data(product_chunk)
            print("-------data_chunk------------",data_chunk)
            push_data = self.env['update.qty.log']._push_qty_to_listing_mirror(data_chunk, integration_name="Push QTY API Integrations with Listing Mirror")
            print("-------push_data------------",push_data)

            # log_vals = []
            # for entry in data_chunk:
            #     print("-------entry['product_id']------------", entry['product_id'])
            #     log_vals.append({
            #         'order_qty':0,
            #         'pushed_qty': entry['quantity'],
            #         'kit_product': False,
            #         'product_id': entry['product_id'],
            #     })
            #
            # print("-------log_vals------------", log_vals)
            # self.env['update.qty.log']._log_qty_push_result(
            #     log_vals, origin='Push QTY API Integrations with Listing Mirror'
            # )
