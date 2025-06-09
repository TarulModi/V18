# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo.exceptions import ValidationError
from odoo import fields, api, models, _, Command


class SaleProductSupplier(models.Model):
    _name = 'sale.product.supplier'
    _description = 'Sale Order Product Supplier'

    sale_id = fields.Many2one('sale.order')
    sale_line_id = fields.Many2one('sale.order.line')
    vendor_id = fields.Many2one('res.partner', required=True)
    price = fields.Float('Price', required=True)
    currency_id = fields.Many2one('res.currency', required=True)

    def create_po(self):
        po_id = self.env['purchase.order.line'].search([('sale_order_line_id', '=', self.sale_line_id.id),
                                                        ('partner_id', '=', self.vendor_id.id),
                                                        ('product_id', '=', self.sale_line_id.product_id.id)])
        if po_id:
            raise ValidationError(_("You can't create multiple purchase order!"))
        vals = {
            'partner_id' : self.vendor_id.id,
            'sale_line_id' : self.sale_line_id.id,
            'order_line' : [(0, 0, {
                    'product_id': self.sale_line_id.product_id.id,
                    'product_qty': self.sale_line_id.product_uom_qty,
                    'price_unit': self.price,
                    'sale_order_line_id': self.sale_line_id.id
                })]
        }
        self.env['purchase.order'].create(vals)
