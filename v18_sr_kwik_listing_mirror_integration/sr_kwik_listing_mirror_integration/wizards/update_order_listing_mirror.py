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
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class UpdateOrderListingMirror(models.TransientModel):
    _name = "update.order.listing.mirror"
    _description = "Update Order Listing Mirror"

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')

    @api.onchange('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.start_date > record.end_date:
                    raise ValidationError("Start Date must be earlier than or equal to End Date.")

    # def update_order_api_integration(self):
    #     start_date = str(self.start_date)
    #     end_date = str(self.end_date)
    #     url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + start_date + "T00:00:00&end_date=" + end_date + "T23:59:59&order_status=Accepted&fulfillment_inventory_source_id=2048"
    #     payload = {}
    #     headers = {
    #         'Authorization': 'Basic ZDVZaUJQRW5XRmRLQURxREJqbEtqUWhJbkc2VDRUR1c6NzJPV0hqSE9meHQ3VlY5bkZHdFRFNjh2M3c0akdVVXE='
    #     }
    #     self.env['sale.order']._api_order_integration(url, headers, payload)
    #     url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + start_date + "T00:00:00&end_date=" + end_date + "T23:59:59&order_status=Unpaid&fulfillment_inventory_source_id=2048"
    #     self.env['sale.order']._api_order_integration(url, headers, payload)
    #     url = "https://api.listingmirror.com/api/v2/orders/?start_date=" + start_date + "T00:00:00&end_date=" + end_date + "T23:59:59&order_status=Pending&fulfillment_inventory_source_id=2048"
    #     self.env['sale.order']._api_order_integration(url, headers, payload)

    def update_order_api_integration(self):
        start_date = str(self.start_date)
        end_date = str(self.end_date)

        kwik_url, kwik_token = self.env['res.config.settings']._url_and_token_listing_mirror()

        headers = {'Authorization': f"Basic {kwik_token}"}
        payload = {}

        order_statuses = ['Accepted', 'Unpaid', 'Pending']
        for status in order_statuses:
            url = f"{kwik_url}orders/?start_date={start_date}T00:00:00&end_date={end_date}T23:59:59&order_status={status}&fulfillment_inventory_source_id=2048"
            self.env['sale.order']._api_order_integration(url, headers, payload)
