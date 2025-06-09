# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

import base64
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class RMASupplier(models.Model):
    _name = 'rma.supplier'
    _description = 'RMA Supplier'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, default='New', tracking=True)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', tracking=True, copy=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    subject = fields.Char(string='Subject', tracking=True, copy=False)
    rma_main_id = fields.Many2one('rma.order', string="RMA No", tracking=True, copy=False)
    reject_reason_id = fields.Many2one('rma.supplier.reason', string='Reject Reason', tracking=True, copy=False)
    status = fields.Selection(
        [
            ('draft', 'Draft'),
            ('approved', 'Approved'),
            ('processing', 'Processing'),
            ('closed', 'Closed'),
            ('reject', 'Rejected')
        ],
        string='Status',
        default='draft',
        tracking=True,
        required=True,
        copy=False
    )

    date = fields.Datetime(string='Date', default=fields.Date.context_today, copy=False)
    deadline = fields.Datetime(string='Deadline', default=fields.Date.context_today, copy=False)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string='Priority', copy=False)

    # Delivery Info
    stock_picking_id = fields.Many2one('stock.picking', string='Delivery Order', copy=False)
    delivery_partner_id = fields.Many2one('res.partner', string='Delivery Partner', copy=False)
    delivery_email = fields.Char(string='Email',  copy=False)
    delivery_phone = fields.Char(string='Phone',  copy=False)
    rma_notes = fields.Text(string='RMA Notes', copy=False)
    is_validate = fields.Boolean(string="Is Validate", copy=False, tracking=True)

    # rma_supplier_order_line_ids = fields.One2many('rma.order.line', 'rma_order_id', copy=False, string="RMA Lines")
    rma_supplier_line_ids = fields.One2many('rma.supplier.line', 'rma_supplier_id', copy=False, string="RMA Lines")

    picking_ids = fields.Many2many('stock.picking', 'picking_rma_supplier_id', 'picking_id', 'rma_id', copy=False,
                                   tracking=True)
    purchase_order_ids = fields.Many2many('purchase.order', 'purchase_supplier_id', 'purchase_id', 'rma_id', copy=False,
                                   tracking=True)

    picking_ids_count = fields.Integer(compute="compute_picking_ids_count", tracking=True)
    purchase_order_ids_count = fields.Integer(compute="compute_purchase_order_ids_count", tracking=True)

    @api.depends('picking_ids')
    def compute_picking_ids_count(self):
        for record in self:
            record.picking_ids_count = self.env['stock.picking'].search_count([('id', 'in', record.picking_ids.ids)])

    @api.depends('purchase_order_ids')
    def compute_purchase_order_ids_count(self):
        for record in self:
            record.purchase_order_ids_count = self.env['purchase.order'].search_count([('id', 'in', record.purchase_order_ids.ids)])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('rma.supplier') or 'New'
        return super().create(vals_list)

    @api.onchange('purchase_order_id')
    def onchange_purchase_order_id(self):
        order_lines_data = [(5, 0)]
        if self.purchase_order_id:
            if self.purchase_order_id.picking_ids:
                picking_id = self.purchase_order_id.picking_ids.filtered(
                    lambda r: r.picking_type_id.code == 'incoming' and r.state == 'done')[:1]
                if picking_id:
                    self.stock_picking_id = picking_id.id
                    self.delivery_partner_id = picking_id.partner_id.id
                    self.delivery_email = picking_id.partner_id.email
                    self.delivery_phone = picking_id.partner_id.phone

            if self.purchase_order_id.order_line:
                for line in self.purchase_order_id.order_line:
                    order_lines_data.append((0, 0, {
                        'product_id': line.product_id.id,
                        'delivery_qty': line.qty_received,
                        'price': line.price_unit,
                        'purchase_line_id': line.id,
                    }))
        self.rma_supplier_line_ids = order_lines_data

    def action_approve(self):
        for record in self:
            picking_list = []
            if not record.stock_picking_id:
                raise UserError("Please select a stock picking before approving.")
            if record.stock_picking_id.state != 'done':
                raise UserError("Stock picking must be in 'Done' state to approve the RMA.")

            if record.rma_main_id:
                rma_order_id = record.rma_main_id.id
            else:
                rma_order_id = False

            if record.company_id and record.company_id.rma_source_picking_type_id:
                rma_source_picking_type_id = record.company_id.rma_source_picking_type_id.id
            else:
                rma_source_picking_type_id = False

            if record.rma_supplier_line_ids:
                picking = self.env['stock.picking'].create({
                    'partner_id': record.purchase_order_id.partner_id.id,
                    'location_id': record.stock_picking_id.picking_type_id.default_location_src_id.id,
                    'picking_type_id': rma_source_picking_type_id,
                    'origin': record.purchase_order_id.name,
                    'purchase_id': record.purchase_order_id.id,
                    'rma_order_id': rma_order_id,
                    'rma_supplier_id': record.id,
                    'move_ids': [(0, 0, {
                        'product_id': return_id.product_id.id,
                        'name': return_id.product_id.display_name,
                        'product_uom_qty': return_id.return_qty,
                        'location_id': record.stock_picking_id.picking_type_id.default_location_src_id.id,
                        'purchase_line_id': return_id.purchase_line_id.id,
                        'rma_supplied_line_id' : return_id.id,
                    }) for return_id in record.rma_supplier_line_ids]
                })
                if picking:
                    picking_list.append(picking.id)

            if picking_list:
                record.picking_ids = [(6, 0, picking_list)]

            record.status = 'approved'

    def action_set_to_draft(self):
        for record in self:
            if record.status == 'draft':
                raise UserError("This record is already in Draft status.")
            record.status = 'draft'

    def action_open_reject_wizard(self):
        return {
            'name': 'Reject Reason',
            'type': 'ir.actions.act_window',
            'res_model': 'reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_model': self._name, 'active_ids': self.ids},
        }

    def action_validate(self):
        if self.rma_supplier_line_ids:
            purchase_list = []
            replace_line_ids = self.rma_supplier_line_ids.filtered(lambda r: r.reason_action == 'replace')
            if self.purchase_order_id:
                partner_id = self.purchase_order_id.partner_id.id
            elif self.stock_picking_id and self.stock_picking_id.partner_id:
                partner_id = self.stock_picking_id.partner_id.id
            else:
                partner_id = self.env.user.partner_id.id
            if replace_line_ids:
                for line in replace_line_ids:
                    purchase_id = self.env['purchase.order'].create({
                        'partner_id' : partner_id,
                        'rma_supplier_id': self.id,
                        'order_line' : [(0, 0, {
                            'product_id': line.replaced_product_id.id,
                            'name': line.replaced_product_id.display_name,
                            'product_qty': line.replaced_qty,
                        })]
                    })
                    if purchase_id:
                        purchase_list.append(purchase_id.id)
            if purchase_list:
                self.purchase_order_ids = [(6, 0, purchase_list)]
        self.is_validate = True

    def action_close(self):
        self.status = 'closed'

    def action_view_receipt(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        return action

    def action_view_purchase_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_rfq")
        action['domain'] = [('id', 'in', self.purchase_order_ids.ids)]
        return action

    def action_send_supplier_email(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Send Email to Supplier',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'rma.supplier',
                'default_rma_ids': self.id,
            }
        }
