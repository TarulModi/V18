# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_contact_person_id = fields.Many2one('res.partner',string="Contact Person", readonly=False)
