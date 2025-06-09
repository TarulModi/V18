# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    diagnosis_id = fields.Many2one('car.diagnosis',tracking=True, copy=False)