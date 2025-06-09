# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################
from odoo.exceptions import UserError
from odoo import fields, api, models, _, Command

SALE_ORDER_STATE = [
    ('draft', "Quotation"),
    ('sent', "Awaited"),
    ('sale', "Accepted"),
    ('cancel', "Not Accepted"),
]


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    order_line = fields.One2many(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=False, auto_join=True)
    state = fields.Selection(
        selection=SALE_ORDER_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')
    vehicle_ids = fields.Many2many('fleet.vehicle', 'fleet_sale_order_rel', 'fleet_id', 'order_id', string="Car Varients")
    vehicle_model_id = fields.Many2one('fleet.vehicle.model', 'Car Model')
    product_supplier_ids = fields.One2many('sale.product.supplier', 'sale_id', copy=False)
    purchase_count = fields.Integer(compute="_compute_purchase_order_count", string='RFQ Count', copy=False, default=0, store=True)
    purchase_ids = fields.Many2many('purchase.order', compute="_compute_purchase_order_count", string='RFQ', copy=False, store=True)
    agent_code = fields.Char("Agent code", copy=False)
    car_reg_no = fields.Char("Car Registration No", copy=False)
    chassis_number = fields.Char("Chassis Number", copy=False)
    location_id = fields.Many2one('stock.location', related='partner_id.location_id', string='Location')
    cancel_reason_id = fields.Many2one('sale.cancel.reason', 'Cancel Reason')
    
    def action_confirm(self):
        for line in self.order_line:
            if line.product_id and line.virtual_available_at_date and not line.price_unit:
                raise UserError(_("Please add Price!"))
        result = super(SaleOrder, self).action_confirm()
        return result

    def action_cancel(self):
        if any(order.locked for order in self):
            raise UserError(_("You cannot cancel a locked order. Please unlock it first."))
        return {
            'name': _("Sale Order Cancel Reason"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'wizard.sale.cancel.reason',
            'target': 'new',
        }

    def open_garage_wp_template(self):
        return {
            'name': _("Garage Whatsapp Template"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'sr.garage.wp.template',
            'target': 'new',
        }

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id and self.partner_id.location_id:
            self.warehouse_id = self.partner_id.location_id.warehouse_id

    @api.depends('order_line.purchase_line_ids.order_id')
    def _compute_purchase_order_count(self):
        for order in self:
            order.purchase_order_count = len(order._get_purchase_orders())
            purchase_ids = self.env['purchase.order'].search([('sale_id', '=', order.id)])
            order.purchase_ids = purchase_ids
            order.purchase_count = len(purchase_ids)

    def action_view_rfq(self):
        return {
            'name': _("RFQ"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'list'),(False, 'form')],
            'res_model': 'purchase.order',
            'domain': [('sale_id', '=', self.id)],
        }

    @api.onchange('order_line')
    def _onchange_product_suppliers(self):
        for rec in self:
            product_supplier_vals = [(5, 0, 0)]
            for line in rec.order_line:
                if line.product_id:
                    if line.virtual_available_at_date < line.product_uom_qty:
                        variant_seller_ids = self.env['product.supplierinfo'].search([('id', 'in', line.product_id.variant_seller_ids.ids)], order="priority")
                        for purchase_supplier in variant_seller_ids:
                            vals = {
                                'sale_line_id': line._origin.id or line.id,
                                'sale_id': rec.id,
                                'vendor_id': purchase_supplier.partner_id.id,
                                'price': purchase_supplier.price,
                                'currency_id': purchase_supplier.currency_id.id or False,
                            }
                            product_supplier_vals.append((0, 0, vals))
            rec.product_supplier_ids = product_supplier_vals

    def open_search_vehicle(self):
        return {
            'name': _("Filter Sale Vehicle Model"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'sr.filter.sale.vehicle.model',
            'target': 'new',
        }

    def copy_data(self, default=None):
        default = dict(default or {})
        default.setdefault('order_line', [])
        vals_list = super().copy_data(default=default)
        return vals_list

    @api.model_create_multi
    def create(self, vals_list):
        sale_ids = super().create(vals_list)
        for rec in sale_ids:
            rec._onchange_product_suppliers()
        return sale_ids

    def open_supplier_info(self):
        return {
            'name': _("Supplier Info"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'wizard.supplier.info',
            'target': 'new',
        }
