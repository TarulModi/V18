# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.exceptions import UserError
from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    kwik_url = fields.Char(string='URL', config_parameter='sr_kwik_listing_mirror_integration.kwik_url')
    kwik_token = fields.Char(string='Token', config_parameter='sr_kwik_listing_mirror_integration.kwik_token')

    def _url_and_token_listing_mirror(self):
        config = self.env['ir.config_parameter'].sudo()
        kwik_url = config.get_param('sr_kwik_listing_mirror_integration.kwik_url')
        kwik_token = config.get_param('sr_kwik_listing_mirror_integration.kwik_token')

        if not kwik_url or not kwik_token:
            raise UserError(_("API URL or Token is not configured."))

        return kwik_url, kwik_token
