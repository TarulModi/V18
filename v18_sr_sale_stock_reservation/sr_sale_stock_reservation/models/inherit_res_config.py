# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    reservation_expiry_days = fields.Integer('Days', default=15, config_parameter='reservation_expiry_days')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        reservation_expiry_days = ICPSudo.get_param('reservation_expiry_days')
        res.update(
            reservation_expiry_days = int(reservation_expiry_days)
        )
        return res
