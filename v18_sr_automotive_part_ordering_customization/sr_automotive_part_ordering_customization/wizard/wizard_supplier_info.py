# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from odoo.osv import expression
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class WizardSupplierInfo(models.TransientModel):
    _name = 'wizard.supplier.info'
    _description = 'Supplier Info'

    supplier_info_line_ids = fields.One2many("wizard.supplier.info.line", "supplier_info_id")

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        product_list = []
        if self.env.context.get('active_id'):
            sale_id = self.env['sale.order'].browse([self.env.context.get('active_id')]).exists()
            if sale_id and sale_id.order_line:
                for line in sale_id.order_line:
                    if line.qty_available_today < line.product_uom_qty:
                        product_list.append((0, 0, {
                            'product_id' : line.product_id.id,
                            'quantity' : line.product_uom_qty - line.qty_available_today,
                            'sale_line_id' : line.id
                        }))
                defaults['supplier_info_line_ids'] = product_list
        return defaults

    def create_purchase_order(self):
        purchase_order_model = self.env['purchase.order']
        purchase_order_line_model = self.env['purchase.order.line']

        vendor_dict = {}
        for line in self.supplier_info_line_ids:
            vendor = line.partner_id
            if vendor not in vendor_dict:
                vendor_dict[vendor] = []
            vendor_dict[vendor].append({
                'product': line.product_id,
                'quantity': line.quantity,
                'sale_order_line_id': line.sale_line_id.id or False,
            })
        purchase_orders = []
        for vendor, products in vendor_dict.items():
            po_vals = {
                'partner_id': vendor.id,
                'order_line': []
            }
            purchase_order = purchase_order_model.create(po_vals)
            if purchase_order:
                sale_id = self.env['sale.order'].browse([self.env.context.get('active_id')]).exists()
                purchase_order.sale_id = sale_id.id
                if purchase_order.partner_id and purchase_order.partner_id.location_id:
                    picking_type = self.env['stock.picking.type'].search([
                        ('code', '=', 'incoming'),
                        ('default_location_dest_id', '=', purchase_order.partner_id.location_id.id)
                    ], limit=1)
                    if picking_type:
                        purchase_order.picking_type_id = picking_type
            for product_data in products:
                purchase_order_line_model.create({
                    'order_id': purchase_order.id,
                    'product_id': product_data['product'].id,
                    'product_qty': product_data['quantity'],
                    'price_unit': product_data['product'].standard_price,
                    'sale_order_line_id': product_data['sale_order_line_id'],
                })
            purchase_orders.append(purchase_order)
        return purchase_orders


class WizardSupplierInfoLine(models.TransientModel):
    _name = 'wizard.supplier.info.line'
    _description = 'Supplier Info Line'

    supplier_info_id = fields.Many2one('wizard.supplier.info')
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float("Quantity")
    brand_id = fields.Many2one('product.brand', "Brand")
    partner_id = fields.Many2one("res.partner", string="Vendor")
    sale_line_id = fields.Many2one("sale.order.line")
