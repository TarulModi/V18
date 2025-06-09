# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    kwik_url = fields.Char(string='URL', config_parameter='sr_kwik_listing_mirror_integration.kwik_url')
    kwik_token = fields.Char(string='Token', config_parameter='sr_kwik_listing_mirror_integration.kwik_token')