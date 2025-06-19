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


class ListingMirrorIntegration(models.TransientModel):
    _name = "update.product.listing.mirror"
    _description = "Listing Mirror Integration"

    sku = fields.Char('SKU')

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

    def _find_uom(self, name):
        return self.env['uom.uom'].sudo().search([('name', '=', name)], limit=1).id or False

    def update_product_api_integration(self):
        # Fetch config parameters
        config = self.env['ir.config_parameter'].sudo()
        kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
        kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')

        integration_name = f"Update Master Product Listing"
        remark = f"Update Product"
        start_date = fields.Datetime.now()
        count = 0

        if not kwik_url or not kwik_token:
            raise UserError(_("API URL or Token is not configured."))

        if not self.sku:
            raise UserError(_("SKU is missing."))

        # Prepare request
        headers = {'Authorization': f"Basic {kwik_token}"}
        url = f"{kwik_url}master-listing/?sku={self.sku.strip()}"

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise UserError(_("Error during API request: %s") % str(e))

        response_json = response.json()
        results = response_json.get('results', [])

        if not results:
            raise UserError(_("No product found in ListingMirror for SKU: %s") % self.sku)

        result = results[0]
        product = self.env['product.product'].search([('default_code', '=', self.sku)], limit=1)

        if not product:
            raise UserError(_('Product not found with this SKU: %s') % self.sku)

        # Prepare image
        image_url = result.get('thumb', '').strip()
        image_data = False
        if image_url:
            try:
                image_data = base64.b64encode(requests.get(image_url, timeout=5).content)
            except Exception:
                image_data = False  # Optionally log or notify image load failure

        # Default category fallback
        category = self.env['product.category'].search([], limit=1)

        price = float(result.get('price') or 0.0)
        cost = float(result.get('cost') or 0.0)

        # Write values
        product.write({
            'name': result.get('variation_title'),
            'type': 'consu',
            'is_storable': True,
            'asin': result.get('asin'),
            'barcode': result.get('upc'),
            'upc': result.get('upc'),
            'mpn': result.get('mpn'),
            'categ_id': category.id if category else False,
            'lst_price': price,
            'standard_price': cost,
            'uom_id': self.env['uom.uom'].search([('name', '=', 'Units')], limit=1).id,
            'uom_po_id': self.env['uom.uom'].search([('name', '=', 'Units')], limit=1).id,
            'weight': result.get('shipping_weight'),
            'shipping_weight_uom': self._find_uom(result.get('shipping_weight_unit_of_measure')),
            'shipping_length': result.get('item_shipping_length'),
            'shipping_width': result.get('item_shipping_width'),
            'shipping_height': result.get('item_shipping_height'),
            'shipping_uom': self._find_uom(result.get('item_shipping_unit_of_measure')),
            'image_1920': image_data,
            'listing_mirror_id': result.get('listing_id')
        })
        end_date = fields.Datetime.now()
        count += len(product)
        if product:
            self._log_details_integration(integration_name, remark, count, start_date, end_date, product.ids)

    def _log_details_integration(self, integration_name, remark, count, start_date, end_date, new_products):
        self.env['integration.log.details'].create({
            'integration_name': integration_name,
            'remark': remark,
            'count': count,
            'start_date': start_date,
            'end_date': end_date,
            'product_ids': [(6, 0, new_products)],
        })