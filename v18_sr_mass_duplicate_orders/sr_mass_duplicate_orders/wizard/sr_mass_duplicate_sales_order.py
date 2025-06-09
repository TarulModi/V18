# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo import api, fields, models, _


class srMassDuplicateSalesOrders(models.TransientModel):
    _name = "sr.mass.duplicate.sales.order"

    def sr_duplicate_sales_orders(self):
        sale = self.env['sale.order'].browse(self._context.get("active_ids",[]))
        for rec in sale:
            rec.copy()

