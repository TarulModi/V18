# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo import fields, api, models, _, Command


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', "Brand")

    def view_po_detail(self):
        return {
            'name': _("Supplier Details"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'wizard.sale.line.po',
            'target': 'new',
            'context': {"sale_line_id": self.id},
        }
