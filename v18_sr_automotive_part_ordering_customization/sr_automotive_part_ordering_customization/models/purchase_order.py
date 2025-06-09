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


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', copy=False)
    location_id = fields.Many2one('stock.location', related='partner_id.location_id', string='Location')
    cancel_reason_id = fields.Many2one('purchase.cancel.reason', 'Cancel Reason')

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id and self.partner_id.location_id:
            picking_type = self.env['stock.picking.type'].search([
                ('code', '=', 'incoming'),
                ('default_location_dest_id', '=', self.partner_id.location_id.id)
            ], limit=1)
            if picking_type:
                self.picking_type_id = picking_type

    def button_confirm(self):
        for line in self.order_line:
            if line.product_id and not line.price_unit:
                raise UserError(_("Please add Price!"))
        result = super(PurchaseOrder, self).button_confirm()
        for order in self.picking_ids:
            if order.move_ids_without_package:
                for rec in order.move_ids_without_package:
                    rec.quantity = rec.product_uom_qty
            order.button_validate()
        return result

    # Override base function
    def button_cancel(self):
        purchase_orders_with_invoices = self.filtered(lambda po: any(i.state not in ('cancel', 'draft') for i in po.invoice_ids))
        if purchase_orders_with_invoices:
            raise UserError(_("Unable to cancel purchase order(s): %s. You must first cancel their related vendor bills.", format_list(self.env, purchase_orders_with_invoices.mapped('display_name'))))
        # self.write({'state': 'cancel', 'mail_reminder_confirmed': False})
        return {
            'name': _("Purchase Order Cancel Reason"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'wizard.purchase.cancel.reason',
            'target': 'new',
        }

    def open_vendor_wp_template(self):
        return {
            'name': _("Vendor Whatsapp Template"),
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
            'res_model': 'sr.vendor.wp.template',
            'target': 'new',
        }
