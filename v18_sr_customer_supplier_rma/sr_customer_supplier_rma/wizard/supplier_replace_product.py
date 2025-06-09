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
from odoo.exceptions import ValidationError


class SupplierReplaceProduct(models.TransientModel):
    _name = 'supplier.replace.product'
    _description = 'Supplier Replace Product'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    qty = fields.Float("QTY")
    is_invoice = fields.Boolean("Create Invoice")

    def button_submit(self):
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        records = self.env[active_model].browse(active_ids)

        for record in records:
            if record.return_qty < self.qty:
                raise ValidationError(_("Repalce quantity should be less or equal to return quantity."))
            record.write({
                'replaced_product_id': self.product_id.id,
                'replaced_qty': self.qty,
                'replaced_is_invoice' : self.is_invoice
            })

        return {'type': 'ir.actions.act_window_close'}
