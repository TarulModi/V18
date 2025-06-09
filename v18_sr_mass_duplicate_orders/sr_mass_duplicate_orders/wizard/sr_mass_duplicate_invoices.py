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
from odoo.exceptions import UserError


class srMassDuplicateInvoices(models.TransientModel):
    _name = "sr.mass.duplicate.invoices"

    def sr_duplicate_invoices(self):
        account = self.env['account.move'].browse(self._context.get("active_ids",[]))
        for rec in account:
            rec.copy()