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


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def custom_button_set_to_draft(self):
        self.state = 'draft'
        for a in self.move_ids_without_package:
            a.state = 'draft'
        return

    # def button_validate(self):
    #     res = super(StockPicking, self).button_validate()
    #     for pick in self:
    #         if pick.picking_type_code == 'incoming' or pick.picking_type_code == 'internal':
    #             for line in pick.move_ids_without_package:
    #                 url = "https://api.listingmirror.com/api/v2/inventory/"
    #                 loc_ids = self.env['stock.location'].search([('usage', '=', 'internal'), ('exclude_location', '=', False), ('name', '!=', 'Stock')])
    #                 qty = 0
    #                 for loc in loc_ids:
    #                     if loc.name != 'Stock' and not loc.exclude_location:
    #                         qty += self.env['stock.quant']._get_available_quantity(line.product_id, loc)
    #                 if qty<=0:
    #                     return res
    #                 payload = json.dumps([
    #                     {
    #                         "sku": line.product_id.default_code,
    #                         "quantity": qty
    #                     }
    #                 ])
    #                 headers = {
    #                     'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE=',
    #                     'Content-Type': 'application/json'
    #                 }
    #                 print ("=======payload",payload)
    #                 response = requests.request("PUT", url, headers=headers, data=payload)
    #                 response_json = response.json()
    #                 print("===button_validate===response_json", response_json)
    #                 print("===button_validate=====not response_json.errors", not response_json.get('errors'))
    #                 if not response_json.get('errors'):
    #                     self.env['update.qty.log'].create({
    #                         'name': 'Purchase Order Created',
    #                         'origin': 'Purchase Order' + str(pick.purchase_id.name),
    #                         'purchase_order_id': pick.purchase_id.id,
    #                         'picking_id': pick.id,
    #                         'qty': line.quantity_done,
    #                         'pushed_qty': qty,
    #                         'product_id': line.product_id.id
    #                     })
    #                 else:
    #                     raise UserError(
    #                         _('Error From Listing mirror for push qty \n' + str(response_json.get('errors'))))
    #
    #     return res

    def button_validate(self):
        res = super(StockPicking, self).button_validate()

        for pick in self:
            if pick.picking_type_code in ('incoming', 'internal'):
                products_to_update = pick.move_ids_without_package.mapped('product_id')

                if products_to_update:
                    data_chunk = self.env['update.qty.log']._prepare_qty_data(products_to_update)
                    self.env['update.qty.log']._push_qty_to_listing_mirror(data_chunk,
                                                                           integration_name="Purchase Order Created")

                    for line in pick.move_ids_without_package:
                        product_id = line.product_id.id
                        product_data = next((item for item in data_chunk if item["product_id"] == product_id), None)
                        if product_data:
                            self.env['update.qty.log'].create({
                                'name': 'Purchase Order Created',
                                'origin': 'Purchase Order ' + str(pick.purchase_id.name),
                                'purchase_order_id': pick.purchase_id.id,
                                'picking_id': pick.id,
                                'qty': line.quantity,
                                'pushed_qty': product_data['quantity'],
                                'product_id': product_id,
                                'move_id': line.id,
                            })

        return res