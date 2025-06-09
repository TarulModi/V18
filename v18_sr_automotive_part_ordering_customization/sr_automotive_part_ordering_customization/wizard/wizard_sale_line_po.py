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


class wizardSaleLinePO(models.TransientModel):
    _name = 'wizard.sale.line.po'
    _desciption = 'Sale Line PO'

    def _default_po_line(self):
        if self.env.context.get('sale_line_id'):
            sale_line_id = self.env['sale.order.line'].browse([self.env.context.get('sale_line_id')]).exists()
            if sale_line_id:
                po_line_ids = self.env['purchase.order.line'].search([('sale_order_line_id', '=', sale_line_id.id),
                                                                      ('product_id', '=', sale_line_id.product_id.id)])
                return [(6, 0, po_line_ids.ids)]
        return []

    def _default_product_supplier(self):
        if self.env.context.get('sale_line_id'):
            sale_line_id = self.env['sale.order.line'].browse([self.env.context.get('sale_line_id')]).exists()
            if sale_line_id and sale_line_id.product_id:
                return [(6, 0, sale_line_id.product_id.product_variant_seller_ids.ids)]
        return []

    po_line_ids = fields.Many2many('purchase.order.line', default=_default_po_line)
    product_variant_seller_ids = fields.Many2many('product.supplierinfo', default=_default_product_supplier)
