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


class srMassDuplicatePurchaseOrder(models.TransientModel):
    _name = "sr.mass.duplicate.purchase.order"
        
    def sr_duplicate_purchase_orders(self):
        po = self.env['purchase.order'].browse(self._context.get("active_ids",[]))
        for rec in po:
            rec.copy()
