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
import requests
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class srupdateQtyLog(models.Model):
    _name = "update.qty.log"
    _description = "Update QTY Log"
    _rec_name = "name"
    
    name = fields.Char('Integration Name', required=True)
    sales_order_id = fields.Many2one('sale.order',string='Sales Order Reference')
    purchase_order_id = fields.Many2one('purchase.order',string='Purchase Order Reference')
    picking_id = fields.Many2one('stock.picking',string="Picking Order Reference")
    # inventory_adjustment_id = fields.Many2one('stock.inventory',string="Inventory Adjustment Reference")
    move_id = fields.Many2one('stock.move',string="Move Reference")
    qty = fields.Float('QTY')
    pushed_qty = fields.Float('Pushed QTY to Listing Mirror')
    origin = fields.Char('Origin',required=True)
    product_id = fields.Many2one('product.product', string="Product")
    kit_product_id = fields.Many2one('product.product',string='Kit Product')


    def _prepare_qty_data(self, products):
        """Prepares quantity data for the given products."""
        available_qty_by_product = {}
        quants = self.env['stock.quant'].search([
            ('location_id.usage', '=', 'internal'),
            ('location_id.exclude_location', '=', False),
            ('location_id.name', '!=', 'Stock')
        ])
        for quant in quants:
            available_qty_by_product.setdefault(quant.product_id.id, 0)
            available_qty_by_product[quant.product_id.id] += quant.available_quantity

        data_chunk = []
        for product in products:
            data_chunk.append({
                "sku": product.default_code or product.name,
                "quantity": available_qty_by_product.get(product.id, 0),
                "product_id": product.id
            })
        print("---data_chunk--------------data_chunk-----------------------",data_chunk)
        return data_chunk

    def _push_qty_to_listing_mirror(self, data_list, integration_name="Push QTY API Integrations"):
        """Pushes prepared qty data to Listing Mirror and logs."""
        config = self.env['ir.config_parameter'].sudo()
        kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
        kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')

        if not kwik_url or not kwik_token:
            raise UserError(_("API URL or Token is not configured."))

        headers = {
            'Authorization': f"Basic {kwik_token}",
            'Content-Type': 'application/json'
        }
        url = f"{kwik_url}inventory/"

        # update_qty_list = []
        for entry in data_list:
            payload = json.dumps(entry)
            # response = requests.request("PUT", url, headers=headers, data=payload)
            # response_json = response.json()
            # if response_json.get("errors"):
            #     # raise UserError(_('Error From Listing Mirror: \n%s' % str(response_json.get('errors'))))
            #     remark = 'Error From Listing Mirror: \n%s' % str(response_json.get('errors'))
            #     self.env['integration.error.log']._log_integration_error(str(response_json.get('errors')), integration_name, remark)

            # update_qty_list.append({
            #     'name': integration_name,
            #     'origin': integration_name,
            #     'qty': entry['quantity'],
            #     'pushed_qty': entry['quantity'],
            #     'product_id': False,
            #     'kit_product_id': False,
            # })
        return True

    def _log_qty_push_result(self, log_val, origin='Manual Push', sales_order=False):
        for record in log_val:
            print("---record.get('product_id')-------------------",record.get('product_id'), type(record.get('product_id')))
            product_id = self.env['product.product'].browse(record.get('product_id')).id
            kit_product_id = self.env['product.product'].browse(record.get('kit_product')).id
            print("----product_id--------------",product_id)
            self.env['update.qty.log'].create({
                'name': origin,
                'origin': f"Sales Order {sales_order.name}" if sales_order else origin,
                'sales_order_id': sales_order.id if sales_order else False,
                'qty': record.get('order_qty'),
                'pushed_qty': record.get('pushed_qty'),
                'product_id': product_id if product_id else False,
                'kit_product_id': kit_product_id if kit_product_id else False,
            })


