# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import fields, api, models, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    rma_supplied_line_id = fields.Many2one("rma.supplier.line", copy=False)