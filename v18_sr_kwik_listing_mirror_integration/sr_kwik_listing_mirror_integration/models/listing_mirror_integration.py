# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import logging
from itertools import islice
from odoo.exceptions import UserError
from odoo import fields, models, api, _
import requests, base64, logging, time, random

_logger = logging.getLogger(__name__)


class ListingMirrorIntegration(models.Model):
    _name = "listing.mirror.integration"
    _description = "Listing Mirror Integration"
    _rec_name = "name"

    name = fields.Char('Integration Name')
#     is_fetch_kit_bundle = fields.Boolean('Fetched All Kit bundles?')
    color = fields.Integer('Color')

# Product Integration

    # def _find_uom(self, uom):
    #     if uom:
    #         uom_id = self.env['uom.uom'].search([('name', '=', uom.lower())])
    #         if uom_id:
    #             return uom_id.id
    #         elif uom == 'GR':
    #             uom_id = self.env['uom.uom'].search([('name', '=', 'g')])
    #             return uom_id.id
    #         else:
    #             raise UserError(_('Shipping UOM not found in system ' + str(uom)))
    #     else:
    #         False

    # def _api_master_listing_integration(self, url, headers, payload):
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #     response_json = response.json()
    #     product_list = []
    #     uom_id = self.env['uom.uom'].search([('name', '=', 'Units')]).id
    #     categ_id = self.env['product.category'].search([])[0].id
    #     for result in response_json.get('results'):
    #         product_id = self.env['product.product'].search([('default_code', '=', result.get('sku'))])
    #         if not product_id:
    #             print ("=======result.get('sku')", result.get('sku'))
    #             product_list.append({
    #                 'name':result.get('variation_title'),
    #                 'sale_ok':True,
    #                 'purchase_ok':True,
    #                 'type':'consu',
    #                 'is_storable': True,
    #                 'default_code':result.get('sku'),
    #                 'asin':result.get('asin'),
    #                 'barcode':result.get('upc'),
    #                 'upc':result.get('upc'),
    #                 'mpn':result.get('mpn'),
    #                 'categ_id':categ_id,
    #                 'lst_price':result.get('price'),
    #                 'standard_price':result.get('cost'),
    #                 'uom_id':uom_id,
    #                 'uom_po_id':uom_id,
    #                 'weight':result.get('shipping_weight'),
    #                 'shipping_weight_uom':self._find_uom(result.get('shipping_weight_unit_of_measure')),
    #                 'shipping_length':result.get('item_shipping_length'),
    #                 'shipping_width':result.get('item_shipping_width'),
    #                 'shipping_height':result.get('item_shipping_height'),
    #                 'shipping_uom':self._find_uom(result.get('item_shipping_unit_of_measure')),
    #                 'image_1920': base64.b64encode(requests.get(result.get('thumb').strip()).content).replace(b'\n', b''),
    #                 'listing_mirror_id':result.get('listing_id')
    #             })
    #     if product_list:
    #         product_ids = self.env['product.product'].create(product_list)
    #         print("----product_ids------product_ids--------",product_ids)
    #     if response_json.get('next'):
    #         url = response_json.get('next')
    #         self._api_master_listing_integration(url, headers, payload)
    #     else:
    #         return
    #
    # def fetch_all_master_product_listing(self):
    #     payload = {}
    #     kwik_url = self.env['ir.config_parameter'].sudo().get_param('sr_kwik_listing_mirror_integration.kwik_url', False)
    #     kwik_token = self.env['ir.config_parameter'].sudo().get_param('sr_kwik_listing_mirror_integration.kwik_token', False)
    #
    #     if not kwik_url:
    #         raise UserError(_("API URL is not configured. Please set URL in system parameters."))
    #
    #     if not kwik_token:
    #         raise UserError(_("API token is not configured. Please set Token in system parameters."))
    #
    #     url = f"{kwik_url}master-listing/"
    #
    #     headers = {
    #         'Authorization': f"Basic {kwik_token}"
    #     }
    #     self._api_master_listing_integration(url, headers, payload)

    # def _get_image_base64(self, url):
    #     try:
    #         response = requests.get(url.strip(), timeout=5)  # Lower timeout
    #         if response.status_code == 200:
    #             return base64.b64encode(response.content).decode('utf-8')  # .decode to avoid b'' bytes
    #     except Exception as e:
    #         _logger.warning(f"Image fetch failed for URL {url}: {str(e)}")
    #     return False

    def _get_image_base64(self, url, session=None):
        try:
            if not session:
                session = requests.Session()
            for attempt in range(2):  # Retry once if it fails
                try:
                    response = session.get(url.strip(), timeout=5)
                    if response.status_code == 200:
                        return base64.b64encode(response.content).decode('utf-8')
                except Exception as e:
                    _logger.warning(f"Retry {attempt + 1} - Image fetch failed: {url} - {e}")
                    time.sleep(0.5)
        except Exception as e:
            _logger.warning(f"Image fetch failed permanently: {url} - {str(e)}")
        return None

    def _chunked(self, iterable, size):
        it = iter(iterable)
        return iter(lambda: list(islice(it, size)), [])

    def _find_uom(self, name):
        return self.env['uom.uom'].sudo().search([('name', '=', name)], limit=1).id or False

    def fetch_all_master_product_listing(self):
        kwik_url, kwik_token = self.env['res.config.settings']._url_and_token_listing_mirror()

        headers = {'Authorization': f"Basic {kwik_token}"}
        url = f"{kwik_url}master-listing/"
        all_results = []

        integration_name = f"Master Product Listing"
        remark = f"Created Products"
        start_date = fields.Datetime.now()

        retry_count = 0
        max_retries = 5
        while url:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                all_results.extend(data.get('results', []))
                url = data.get('next')
                retry_count = 0
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429 and retry_count < max_retries:
                    wait_time = 2 ** retry_count + random.uniform(0, 1)
                    time.sleep(wait_time)
                    retry_count += 1
                else:
                    _logger.error(f"API Error: {e}")
                    break

        if not all_results:
            _logger.info("No products found from API.")
            return

        # --- Bulk read existing SKUs ---
        existing_sku_codes = set(map(lambda r: r['default_code'], self.env['product.product'].sudo().search_read(
            [('default_code', '!=', False)],
            fields=['default_code'],
            limit=None
        )))

        uom_id = self.env.ref('uom.product_uom_unit').id
        categ_id = self.env['product.category'].search([], limit=1).id

        new_products = []
        failed_records = []

        # --- Fast image processing using session and skip image if slow ---
        session = requests.Session()

        for result in all_results:
            sku = result.get('sku')
            if not sku or sku in existing_sku_codes:
                continue

            try:
                image_data = None
                thumb_url = result.get('thumb')
                if thumb_url:
                    image_data = self._get_image_base64(thumb_url, session=session) if thumb_url else None
                    # try:
                    #     # img_response = session.get(thumb_url.strip(), timeout=3)
                    #     img_response = requests.get(thumb_url.strip(), timeout=2)
                    #     if img_response.status_code == 200:
                    #         image_data = base64.b64encode(img_response.content).decode('utf-8')
                    # except Exception as e:
                    #     _logger.warning(f"Image fetch failed for SKU {sku}: {e}")

                product_vals = {
                    'name': result.get('variation_title') or 'Unnamed Product',
                    'sale_ok': True,
                    'purchase_ok': True,
                    'type': 'consu',
                    'is_storable': True,
                    'default_code': sku,
                    'asin': result.get('asin'),
                    'barcode': result.get('upc'),
                    'upc': result.get('upc'),
                    'mpn': result.get('mpn'),
                    'categ_id': categ_id,
                    'lst_price': float(result.get('price') or 0.0),
                    'standard_price': float(result.get('cost') or 0.0),
                    'uom_id': uom_id,
                    'uom_po_id': uom_id,
                    'weight': float(result.get('shipping_weight') or 0.0),
                    'shipping_weight_uom': self._find_uom(result.get('shipping_weight_unit_of_measure')),
                    'shipping_length': float(result.get('item_shipping_length') or 0.0),
                    'shipping_width': float(result.get('item_shipping_width') or 0.0),
                    'shipping_height': float(result.get('item_shipping_height') or 0.0),
                    'shipping_uom': self._find_uom(result.get('item_shipping_unit_of_measure')),
                    'image_1920': image_data,
                    'listing_mirror_id': result.get('listing_id'),
                }
                print("---product_vals--------",product_vals)
                new_products.append(product_vals)

            except Exception as e:
                failed_records.append({
                    'sku': sku,
                    'error': str(e),
                    'data': result
                })

        created_count = 0
        if new_products:
            # product_obj = self.env['product.product'].sudo().with_context(
            #     prefetch_fields=False, mail_create_nolog=True, tracking_disable=True, active_test=False
            # )
            product_obj = self.env['product.product'].sudo()
            print("---product_obj--------",product_obj)

            # --- Bulk insert using chunks ---
            with self.env.cr.savepoint():
                for chunk in self._chunked(new_products, 1000):  # or 500 for less load
                    product_obj.create(chunk)
                    created_count += len(chunk)

            # product_obj.flush()
            _logger.info(f"{created_count} products created successfully.")

        end_date = fields.Datetime.now()
        print("--new_products-------new_products------",new_products)
        if new_products:
            self._log_details_integration(integration_name, remark, created_count, start_date, end_date, new_products)

        if failed_records:
            _logger.warning(f"{len(failed_records)} records failed.")
            return {
                'created_count': created_count,
                'failed_count': len(failed_records),
                'failed_records': failed_records
            }

        return {'created_count': created_count, 'failed_count': len(failed_records)}

    def update_product_listing(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_kwik_listing_mirror_integration.action_update_product_from_listing_mirror")
        action['context'] = dict(
            self.env.context,
        )
        return action
        
# Product Kit Integration
    
    # def _product_bundle_kit_receipes_connection(self, url, headers, payload):
    #     response = requests.request("GET", url, headers=headers, data=payload)
    #     response_json = response.json()
    #     integration_name = f"Bundle Kit Integration"
    #     remark = f"Kits"
    #     start_date = fields.Datetime.now()
    #     count = 0
    #     bom_list = []
    #     for main_product in response_json.get('results'):
    #         for recipe in main_product.get('recipes'):
    #             if recipe.get('sku') != main_product.get('sku'):
    #                 product_template_id = self.env['product.template'].search([('default_code', '=', main_product.get('sku'))])
    #                 if not product_template_id:
    #                     # raise UserError(_('Product Not Found With This SKU : ' + str(main_product.get('sku'))))
    #                     self._log_integration_error(main_product.get('sku'), 'Product Not Found')
    #                 existing_bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', product_template_id.id)])
    #                 print ("========existing_bom_id-----------", existing_bom_id)
    #                 if not existing_bom_id:
    #                     bom_id = self.env['mrp.bom'].create({
    #                         'product_tmpl_id':product_template_id.id,
    #                         'product_id':self.env['product.product'].search([('default_code', '=', main_product.get('sku'))]).id,
    #                         'type':'phantom'
    #                         })
    #                     print ("=========bom_id-----------------", bom_id)
    #                     count += len(bom_id)
    #                     bom_list.append(bom_id.id)
    #                     product_template_id.write({
    #                         'purchase_ok':False
    #                         })
    #                     product_id = self.env['product.product'].search([('default_code', '=', recipe.get('sku'))])
    #                     if not product_id:
    #                         # raise UserError(_('Product Not Found With This SKU : ' + str(recipe.get('sku'))))
    #                         self._log_integration_error(recipe.get('sku'), 'Product Not Found')
    #                     if product_id:
    #                         self.env['mrp.bom.line'].create({
    #                             'bom_id':bom_id.id,
    #                             'product_id':product_id.id,
    #                             'product_qty':recipe.get('quantity')
    #                             })
    #                 else:
    #                     existing_products = [a.product_id.id for a in existing_bom_id.bom_line_ids]
    #                     product_id = self.env['product.product'].search([('default_code', '=', recipe.get('sku'))]).id
    #                     print ("=======existing_products", existing_products, product_id)
    #                     print ("=========product.id not in existing_products", product_id not in existing_products)
    #                     if product_id not in existing_products:
    #                         self.env['mrp.bom.line'].create({
    #                         'bom_id':existing_bom_id.id,
    #                         'product_id':product_id,
    #                         'product_qty':recipe.get('quantity')
    #                         })
    #                     count += len(existing_bom_id)
    #                     bom_list.append(existing_bom_id.id)
    #
    #     end_date = fields.Datetime.now()
    #     print("----bom_list-------bom_list-----------",bom_list)
    #     if bom_list:
    #         self._log_details_integration_bom(integration_name, remark, count, start_date, end_date, bom_list)
    #
    #     if response_json.get('next'):
    #         url = response_json.get('next')
    #         self._product_bundle_kit_receipes_connection(url, headers, payload)
    #     else:
    #         return

    def _product_bundle_kit_receipes_connection(self, url, headers, payload):
        integration_name = "Bundle Kit Integration"
        remark = "Kits"
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            response.raise_for_status()
            response_json = response.json()
        except Exception as e:
            # self._log_integration_error("N/A", f"Request failed at URL: {url} - Error: {str(e)}")
            integration_name = 'KIT'
            remark = f"Request failed at URL: {url} - Error: {str(e)}"
            self.env['integration.error.log']._log_integration_error("N/A", integration_name, remark)

            return

        start_date = fields.Datetime.now()
        count = 0
        bom_list = []

        results = response_json.get('results', [])
        if not isinstance(results, list):
            # self._log_integration_error("N/A", "Invalid or missing 'results' in response")
            remark = "Invalid or missing 'results' in response"
            self.env['integration.error.log']._log_integration_error("N/A", integration_name, remark)
            return

        for main_product in results:
            for recipe in main_product.get('recipes', []):
                if recipe.get('sku') != main_product.get('sku'):
                    product_template_id = self.env['product.template'].search(
                        [('default_code', '=', main_product.get('sku'))], limit=1)
                    if not product_template_id:
                        # self._log_integration_error(main_product.get('sku'), 'Product Not Found')
                        remark = "Product Not Found"
                        self.env['integration.error.log']._log_integration_error(main_product.get('sku'), integration_name, remark)
                        continue

                    existing_bom_id = self.env['mrp.bom'].search([('product_tmpl_id', '=', product_template_id.id)],
                                                                 limit=1)
                    if not existing_bom_id:
                        bom_id = self.env['mrp.bom'].create({
                            'product_tmpl_id': product_template_id.id,
                            'product_id': self.env['product.product'].search(
                                [('default_code', '=', main_product.get('sku'))], limit=1).id,
                            'type': 'phantom'
                        })
                        count += 1
                        bom_list.append(bom_id.id)

                        product_template_id.write({'purchase_ok': False})

                        product_id = self.env['product.product'].search([('default_code', '=', recipe.get('sku'))],
                                                                        limit=1)
                        if not product_id:
                            # self._log_integration_error(recipe.get('sku'), 'Product Not Found')
                            remark = "Product Not Found"
                            self.env['integration.error.log']._log_integration_error(recipe.get('sku'), integration_name, remark)
                            continue

                        self.env['mrp.bom.line'].create({
                            'bom_id': bom_id.id,
                            'product_id': product_id.id,
                            'product_qty': recipe.get('quantity')
                        })
                    else:
                        existing_products = [line.product_id.id for line in existing_bom_id.bom_line_ids]
                        product_id = self.env['product.product'].search([('default_code', '=', recipe.get('sku'))],
                                                                        limit=1)
                        if not product_id:
                            # self._log_integration_error(recipe.get('sku'), 'Product Not Found')
                            remark = "Product Not Found"
                            self.env['integration.error.log']._log_integration_error(recipe.get('sku'), integration_name, remark)
                            continue

                        if product_id.id not in existing_products:
                            self.env['mrp.bom.line'].create({
                                'bom_id': existing_bom_id.id,
                                'product_id': product_id.id,
                                'product_qty': recipe.get('quantity')
                            })

                        count += 1
                        bom_list.append(existing_bom_id.id)

        end_date = fields.Datetime.now()

        if bom_list:
            self._log_details_integration_bom(integration_name, remark, count, start_date, end_date, bom_list)

        next_url = response_json.get('next')
        if isinstance(next_url, str) and next_url.strip():
            self._product_bundle_kit_receipes_connection(next_url.strip(), headers, payload)

    def _log_details_integration(self, integration_name, remark, count, start_date, end_date, new_products):
        self.env['integration.log.details'].create({
            'integration_name': integration_name,
            'remark': remark,
            'count': count,
            'start_date': start_date,
            'end_date': end_date,
            'product_ids': [(6, 0, new_products)],
        })

    def _log_details_integration_bom(self, integration_name, remark, count, start_date, end_date, bom_list):
        self.env['integration.log.details'].create({
            'integration_name': integration_name,
            'remark': remark,
            'count': count,
            'start_date': start_date,
            'end_date': end_date,
            'bom_ids': [(6, 0, bom_list)],
        })

    def fetch_all_receipes_listing(self):
        #         if self.is_fetch_kit_bundle:
        #             raise UserError(_('Kit Product Already Integrated.'))
        # url = "https://api.listingmirror.com/api/v2/recipes/"
        # headers = {
        #             'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE='
        #             }

        kwik_url, kwik_token = self.env['res.config.settings']._url_and_token_listing_mirror()

        headers = {'Authorization': f"Basic {kwik_token}"}
        url = f"{kwik_url}recipes/"
        payload = {}
        res = self._product_bundle_kit_receipes_connection(url, headers, payload)
#         self.browse(self._context.get('active_id')).write({
#             'is_fetch_kit_bundle':True
#             })

# Orders Integration

    def fetch_all_orders_listing(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_kwik_listing_mirror_integration.action_update_orders_from_listing_mirror")
        action['context'] = dict(
            self.env.context,
        )
        return action
        
# push qty to listing mirror

    def push_qty_to_orders_listing(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_kwik_listing_mirror_integration.action_push_qty_to_listing_mirror")
        action['context'] = dict(
            self.env.context,
        )
        return action

