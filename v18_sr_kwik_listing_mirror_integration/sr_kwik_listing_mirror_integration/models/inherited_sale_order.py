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
import pytz
import zulu
import base64
import logging
import requests
from dateutil import parser
from dateutil import parser as zulu
from odoo.exceptions import UserError
from odoo import fields, models, api, _
from datetime import datetime, date,timedelta
from odoo.tools.misc import formatLang, get_lang
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    listing_mirror_order_id = fields.Char('Listing Mirror Order Id')
    alternate_market_order_id = fields.Char('Alternate Market Order ID')
    alternate_market_order_id_2 = fields.Char('Alternate Market Order ID 2')
    lm_status = fields.Selection([('Pending', 'Pending'), ('Unpaid', 'Unpaid'), ('Accepted', 'Accepted'), ('Cancelled', 'Cancelled'),('Error', 'Error')], string="Listing Mirror Status")
    channel_order_status = fields.Selection([('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Shipping', 'Shipping'),  ('Delivered', 'Delivered')], string="Channel Order Status")
    is_channel_fulfillment = fields.Boolean('Fulfilled By Channel?')
    error_msg = fields.Char('Error Message')


    # def action_cron_check_order_status(self):
    #     sale_order = self.env['sale.order'].search([('lm_status', 'in', ['Pending', 'Unpaid'])])
    #     print ("========sale_order",sale_order)
    #     for order in sale_order:
    #         url = "https://api.listingmirror.com/api/v2/orders/?search_value=" + order.name
    #         print ("======url", url)
    #         payload = {}
    #         headers = {
    #                 'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE='
    #                 }
    #         response = requests.request("GET", url, headers=headers, data=payload)
    #         response_json = response.json()
    #         order_response = response_json.get('results')
    #         print ("====================order",order)
    #         print ("=======order_response",order_response)
    #         if order_response:
    #             if order_response[0].get('order_status') == 'Cancelled':
    #                 vals = []
    #                 log_val = []
    #                 print ("==========order",order)
    #                 order.action_cancel()
    #                 for line in order.order_line:
    #                     if line.product_id.bom_ids:
    #                         for bom_line in line.product_id.bom_ids.bom_line_ids:
    #                             loc_ids = self.env['stock.location'].search([('usage', '=', 'internal')])
    #                             qty = 0
    #                             for loc in loc_ids:
    #                                 if loc.name != 'Stock' and not loc.exclude_location:
    #                                     qty += self.env['stock.quant']._get_available_quantity(bom_line.product_id, loc)
    #                             vals.append({
    #                                 'sku':bom_line.product_id.default_code,
    #                                 "quantity": qty
    #                                 })
    #                             log_val.append({
    #                                 'product':bom_line.product_id,
    #                                 'kit_product':line.product_id,
    #                                 'order_qty':line.product_uom_qty,
    #                                 'pushed_qty':qty
    #                                 })
    #                     else:
    #                         if line.product_id.type != 'service':
    #                             loc_ids = self.env['stock.location'].search([('usage', '=', 'internal')])
    #                             qty = 0
    #                             for loc in loc_ids:
    #                                 if loc.name != 'Stock' and not loc.exclude_location:
    #                                     qty += self.env['stock.quant']._get_available_quantity(line.product_id, loc)
    #                             vals.append({
    #                                 "sku": line.product_id.default_code,
    #                                 "quantity": qty
    #                            })
    #                             log_val.append({
    #                                 'product':line.product_id,
    #                                 'order_qty':line.product_uom_qty,
    #                                 'pushed_qty':qty
    #                             })
    #                 payload = json.dumps(vals)
    #                 url = "https://api.listingmirror.com/api/v2/inventory/"
    #                 headers = {
    #                             'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE=',
    #                             'Content-Type': 'application/json'
    #                             }
    #                 response = requests.request("PUT", url, headers=headers, data=payload)
    #                 response_json = response.json()
    #                 if not response_json.get('errors'):
    #                     for record in log_val:
    #                         self.env['update.qty.log'].create({
    #                             'name':'Sales Order Cancelled',
    #                             'origin':'Sales Order' + str(self.name),
    #                             'sales_order_id':order.id,
    #                             'qty':record.get('order_qty'),
    #                             'pushed_qty':record.get('pushed_qty'),
    #                             'product_id':record.get('kit_product').id if record.get('kit_product') else False,
    #                             'kit_product_id':record.get('product').id if record.get('product') else False,
    #                             })
    #                 else:
    #                     raise UserError(_('Error From Listing mirror for push qty \n' + str(response_json.get('errors'))))
    #             order.write({
    #                 'lm_status':order_response[0].get('order_status')
    #                 })

    # def _api_order_integration(self, url, headers, payload):
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #     response_json = response.json()
    #     print ("======url", url)
    #     print ("======count", response_json.get('count'))
    #     for order in response_json.get('results'):
    #         order_id = self.search([('name', '=', order.get('market_order_id'))])
    #         if not order_id:
    #             order_dt = zulu.parse(order.get('order_datetime'))
    #             date_order = order_dt if order_dt.tzinfo is None else order_dt.replace(tzinfo=None)
    #             new_order_id = self.create({
    #                 'partner_id':self.env['res.partner'].search([('integration_config_id', '=', order.get('integration_config_id'))]).id,
    #                 'name':order.get('market_order_id'),
    #                 'listing_mirror_order_id':order.get('order_id'),
    #                 'alternate_market_order_id':order.get('alternate_market_order_id'),
    #                 'alternate_market_order_id_2':order.get('alternate_market_order_id_2'),
    #                 'date_order':date_order,
    #                 'lm_status':order.get('order_status')
    #                 })
    #             for line in order.get('order_items'):
    #                 discount = 0.0
    #                 if line.get('shipping_discount'):
    #                     discount += float(line.get('shipping_discount'))
    #                 if line.get('item_discount'):
    #                     discount += float(line.get('item_discount'))
    #                 main_product = self.env['product.product'].search([('default_code', '=', line.get('sku'))])
    #                 if not main_product:
    #                     new_order_id.lm_status = 'Error'
    #                     new_order_id.error_msg = line.get('sku')+'Not Available in Odoo'
    #                 else:
    #                     self.env['sale.order.line'].create({
    #                         'product_id':main_product.id,
    #                         'product_uom_qty':line.get('quantity'),
    #                         'price_unit':float(line.get('price'))/line.get('quantity'),
    #                         'discount':discount,
    #                         'order_id':new_order_id.id
    #                         })
    #                     if line.get('shipping_price'):
    #                         self.env['sale.order.line'].create({
    #                         'product_id':self.env['product.product'].search([('default_code', '=', 'ship_price')]).id,
    #                         'product_uom_qty':1,
    #                         'price_unit':line.get('shipping_price'),
    #                         'order_id':new_order_id.id
    #                         })
    #                     if line.get('shipping_tax'):
    #                         self.env['sale.order.line'].create({
    #                         'product_id':self.env['product.product'].search([('default_code', '=', 'ship_tax')]).id,
    #                         'product_uom_qty':1,
    #                         'price_unit':line.get('shipping_tax'),
    #                         'order_id':new_order_id.id
    #                         })
    #                     if line.get('tax'):
    #                         self.env['sale.order.line'].create({
    #                         'product_id':self.env['product.product'].search([('default_code', '=', 'produ_tax')]).id,
    #                         'product_uom_qty':1,
    #                         'price_unit':line.get('tax'),
    #                         'order_id':new_order_id.id
    #                         })
    #                     if line.get('gift_warp_price'):
    #                         self.env['sale.order.line'].create({
    #                         'product_id':self.env['product.product'].search([('default_code', '=', 'gift_price')]).id,
    #                         'product_uom_qty':1,
    #                         'price_unit':line.get('gift_warp_price'),
    #                         'order_id':new_order_id.id
    #                         })
    #                     if line.get('gift_warp_tax'):
    #                         self.env['sale.order.line'].create({
    #                         'product_id':self.env['product.product'].search([('default_code', '=', 'gift_tax')]).id,
    #                         'product_uom_qty':1,
    #                         'price_unit':line.get('gift_warp_tax'),
    #                         'order_id':new_order_id.id
    #                         })
    #             for line in new_order_id.order_line:
    #                 if line.product_id.bom_ids:
    #                     for bom_line in line.product_id.bom_ids.bom_line_ids:
    #                         qty = bom_line.product_id.qty_available - (bom_line.product_id.outgoing_qty + (
    #                                     bom_line.product_qty * line.product_uom_qty))
    #                         if qty < 0:
    #                             new_order_id.lm_status = 'Error'
    #                             new_order_id.error_msg = "QTY is less than zero"
    #                 else:
    #                     if line.product_id.type != 'service':
    #                         qty = line.product_id.qty_available - (line.product_id.outgoing_qty + line.product_uom_qty)
    #                         if qty < 0:
    #                             new_order_id.lm_status = 'Error'
    #                             new_order_id.error_msg = "QTY is less than zero"
    #             if new_order_id.lm_status != 'Error':
    #                 new_order_id.action_confirm()
    #
    #     if response_json.get('next'):
    #         url = response_json.get('next')
    #         self._api_order_integration(url, headers, payload)
    #     else:
    #         return
    #
    # def action_cron_order_api_integration(self):
    #     current_date = str(datetime.today().date())
    #     previous_date = str(datetime.today().date() - timedelta(days=1))
    #     payload = {}
    #     # headers = {
    #     #             'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE='
    #     #             }
    #
    #     config = self.env['ir.config_parameter'].sudo()
    #     kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
    #     kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')
    #
    #     if not kwik_url or not kwik_token:
    #         raise UserError(_("API URL or Token is not configured."))
    #
    #     headers = {'Authorization': f"Basic {kwik_token}"}
    #
    #
    #     # url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + previous_date + "T00:00:00&end_date=" + current_date + "T23:59:59&order_status=Accepted&fulfillment_inventory_source_id=2048"
    #     url = f"{kwik_url}orders/?start_date={previous_date}T00:00:00&end_date={current_date}T23:59:59&order_status=Accepted&fulfillment_inventory_source_id=2048"
    #     self._api_order_integration(url, headers, payload)
    #
    #     url = f"{kwik_url}orders/?start_date={previous_date}T00:00:00&end_date={current_date}T23:59:59&order_status=Unpaid&fulfillment_inventory_source_id=2048"
    #     # url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + previous_date + "T00:00:00&end_date=" + current_date + "T23:59:59&order_status=Unpaid&fulfillment_inventory_source_id=2048"
    #     self._api_order_integration(url, headers, payload)
    #
    #     url = f"{kwik_url}orders/?start_date={previous_date}T00:00:00&end_date={current_date}T23:59:59&order_status=Pending&fulfillment_inventory_source_id=2048"
    #     # url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + previous_date + "T00:00:00&end_date=" + current_date + "T23:59:00&order_status=Pending&fulfillment_inventory_source_id=2048"
    #     self._api_order_integration(url, headers, payload)

    def _create_special_line(self, order_id, code, quantity, price):
        """Helper to create a sale order line with a specific product code"""
        product = self.env['product.product'].search([('default_code', '=', code)], limit=1)
        if product:
            self.env['sale.order.line'].create({
                'product_id': product.id,
                'product_uom_qty': quantity,
                'price_unit': price,
                'order_id': order_id.id
            })

    def _api_order_integration(self, url, headers, payload):
        while url:
            print("======url", url)
            response = requests.get(url, headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()

            _logger.info("Fetching orders from: %s", url)
            _logger.info("Order count: %s", response_json.get('count'))

            for order in response_json.get('results', []):
                if self.search([('name', '=', order.get('market_order_id'))], limit=1):
                    continue  # Order already exists

                partner = self.env['res.partner'].search(
                    [('integration_config_id', '=', order.get('integration_config_id'))], limit=1)

                order_dt = zulu.parse(order.get('order_datetime'))
                date_order = order_dt if order_dt.tzinfo is None else order_dt.replace(tzinfo=None)

                new_order_id = self.create({
                    'partner_id': partner.id if partner else False,
                    'name': order.get('market_order_id'),
                    'listing_mirror_order_id': order.get('order_id'),
                    'alternate_market_order_id': order.get('alternate_market_order_id'),
                    'alternate_market_order_id_2': order.get('alternate_market_order_id_2'),
                    'date_order': date_order,
                    'lm_status': order.get('order_status'),
                })

                for line in order.get('order_items', []):
                    discount = float(line.get('shipping_discount') or 0.0) + float(line.get('item_discount') or 0.0)
                    main_product = self.env['product.product'].search([('default_code', '=', line.get('sku'))], limit=1)

                    if not main_product:
                        new_order_id.write({
                            'lm_status': 'Error',
                            'error_msg': f"{line.get('sku')} Not Available in Odoo"
                        })
                        continue

                    self.env['sale.order.line'].create({
                        'product_id': main_product.id,
                        'product_uom_qty': line.get('quantity'),
                        'price_unit': float(line.get('price')) / line.get('quantity'),
                        'discount': discount,
                        'order_id': new_order_id.id
                    })

                    # Create additional charge lines
                    self._create_special_line(new_order_id, 'ship_price', 1, line.get('shipping_price', 0.0))
                    self._create_special_line(new_order_id, 'ship_tax', 1, line.get('shipping_tax', 0.0))
                    self._create_special_line(new_order_id, 'produ_tax', 1, line.get('tax', 0.0))
                    self._create_special_line(new_order_id, 'gift_price', 1, line.get('gift_warp_price', 0.0))
                    self._create_special_line(new_order_id, 'gift_tax', 1, line.get('gift_warp_tax', 0.0))

                # Check stock availability
                for line in new_order_id.order_line:
                    if line.product_id.bom_ids:
                        for bom_line in line.product_id.bom_ids[0].bom_line_ids:
                            qty = bom_line.product_id.qty_available - (
                                    bom_line.product_id.outgoing_qty + (bom_line.product_qty * line.product_uom_qty))
                            if qty < 0:
                                new_order_id.write({
                                    'lm_status': 'Error',
                                    'error_msg': "QTY is less than zero"
                                })
                                break
                    elif line.product_id.type != 'service':
                        qty = line.product_id.qty_available - (line.product_id.outgoing_qty + line.product_uom_qty)
                        if qty < 0:
                            new_order_id.write({
                                'lm_status': 'Error',
                                'error_msg': "QTY is less than zero"
                            })
                            break

                if new_order_id.lm_status != 'Error':
                    try:
                        new_order_id.action_confirm()
                    except Exception as e:
                        new_order_id.write({'lm_status': 'Error', 'error_msg': str(e)})

            url = response_json.get('next')
            print("===2222222222222222===url", url)

    def action_cron_order_api_integration(self):
        current_date = datetime.today().date()
        previous_date = current_date - timedelta(days=1)

        config = self.env['ir.config_parameter'].sudo()
        kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
        kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')

        if not kwik_url or not kwik_token:
            raise UserError(_("API URL or Token is not configured."))

        headers = {'Authorization': f"Basic {kwik_token}"}
        payload = {}

        order_statuses = ['Accepted', 'Unpaid', 'Pending']
        for status in order_statuses:
            url = f"{kwik_url}orders/?start_date={previous_date}T00:00:00&end_date={current_date}T23:59:59&order_status={status}&fulfillment_inventory_source_id=2048"
            self._api_order_integration(url, headers, payload)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    channel_order_line_status = fields.Selection(
        [('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Unshipped', 'Unshipped'), ('Unshipped', 'Unshipped'), ('Delivered', 'Delivered')],
        string="Channel Order line Status")


    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )
        name = ''
        if product.barcode:
            name += '[' + product.barcode + ']'
        name += product.name
        if product.description_sale:
            name += '\n' + product.description_sale 
        vals.update(name=name)
#         vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False

        return result

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit - line.discount
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
