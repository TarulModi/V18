# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Sitaram Solutions (<https://sitaramsolutions.in/>).
#
#    For Module Support : info@sitaramsolutions.in  or Skype : contact.hiren1188
#
##############################################################################

from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class rmaOrder(models.Model):
    _name = 'rma.order'
    _description = 'RMA Order'
    _order = 'name desc'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    name = fields.Char(string='RMA Reference', required=True, copy=False, readonly=True, default='New', tracking=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', tracking=True, copy=False)
    subject = fields.Char(string='Subject', tracking=True, copy=False)
    crm_team_id = fields.Many2one('crm.team', string='Sales Channel', tracking=True, copy=False)

    date = fields.Datetime(string='Date', default=fields.Date.context_today, copy=False, tracking=True)
    deadline = fields.Datetime(string='Deadline', default=fields.Date.context_today, copy=False, tracking=True)
    user_id = fields.Many2one('res.users', string='Responsible', copy=False, tracking=True)
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Very High')
    ], string='Priority', copy=False, tracking=True)

    # Delivery Info
    stock_picking_id = fields.Many2one('stock.picking', string='Delivery Order', copy=False, tracking=True)
    delivery_partner_id = fields.Many2one('res.partner', string='Delivery Partner', copy=False, tracking=True)
    delivery_email = fields.Char(string='Email', related='delivery_partner_id.email', copy=False, tracking=True)
    delivery_phone = fields.Char(string='Phone', related='delivery_partner_id.phone', copy=False, tracking=True)

    # Invoice Info
    invoice_partner_id = fields.Many2one('res.partner', string='Invoice Partner', copy=False, tracking=True)
    invoice_email = fields.Char(string='Invoice Email', related='invoice_partner_id.email', copy=False, tracking=True)
    invoice_phone = fields.Char(string='Invoice Phone', related='invoice_partner_id.phone', copy=False, tracking=True)

    rma_order_line_ids = fields.One2many('rma.order.line', 'rma_order_id', copy=False, string="RMA Lines")
    rma_replaced_product_ids = fields.One2many('rma.replaced.product', 'rma_order_id', copy=False, string="Replaced Products")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('supplier_rma', 'Supplier RMA'),
        ('submit', 'Submitted'),
        ('approved', 'Approve'),
        ('processing', 'Processing'),
        ('reject', 'Rejected'),
        ('close', 'Closed'),
    ], string='Status', default="draft", copy=False, tracking=True)

    is_validate = fields.Boolean("is_validate", copy=False, tracking=True)
    validate = fields.Boolean("Validate", copy=False, tracking=True)
    picking_ids = fields.Many2many('stock.picking', 'picking_rma_order_id', 'picking_id', 'rma_id', copy=False, tracking=True)
    invoice_ids = fields.Many2many('account.move', 'move_rma_order_id', 'move_id', 'rma_id', copy=False, tracking=True)
    sale_order_ids = fields.Many2many('sale.order', 'sale_rma_order_id', 'sale_id', 'rma_id', copy=False, tracking=True)

    picking_ids_count = fields.Integer(compute="compute_picking_ids_count", tracking=True)
    invoice_ids_count = fields.Integer(compute="compute_invoice_ids_count", tracking=True)
    sale_order_ids_count = fields.Integer(compute="compute_sale_order_ids_count", tracking=True)
    supplier_ids_count = fields.Integer(compute="compute_supplier_ids_count", tracking=True)

    rma_notes = fields.Text(string='RMA Notes', copy=False)

    @api.depends('picking_ids')
    def compute_picking_ids_count(self):
        for record in self:
            record.picking_ids_count = self.env['stock.picking'].search_count([('id', 'in', record.picking_ids.ids)])

    @api.depends('invoice_ids')
    def compute_invoice_ids_count(self):
        for record in self:
            record.invoice_ids_count = self.env['account.move'].search_count([('id', 'in', record.invoice_ids.ids)])

    @api.depends('sale_order_ids')
    def compute_sale_order_ids_count(self):
        for record in self:
            record.sale_order_ids_count = self.env['sale.order'].search_count([('id', 'in', record.sale_order_ids.ids)])

    def compute_supplier_ids_count(self):
        for record in self:
            record.supplier_ids_count = self.env['rma.supplier'].search_count([('rma_main_id', '=', record.id)])

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('rma.order') or 'New'
        return super().create(vals_list)

    @api.onchange('sale_order_id')
    def onchange_sale_order(self):
        order_lines_data = [(5, 0)]
        if self.sale_order_id:
            if self.sale_order_id.picking_ids:
                picking_id = self.sale_order_id.picking_ids.filtered(
                    lambda r: r.picking_type_id.code == 'outgoing' and r.state == 'done')[:1]
                if picking_id:
                    self.stock_picking_id = picking_id.id

            self.crm_team_id = self.sale_order_id.team_id.id
            self.user_id = self.sale_order_id.user_id.id
            self.delivery_partner_id = self.sale_order_id.partner_shipping_id.id
            self.invoice_partner_id = self.sale_order_id.partner_invoice_id.id

            if self.sale_order_id.order_line:
                for line in self.sale_order_id.order_line:
                    order_lines_data.append((0, 0, {
                        'product_id': line.product_id.id,
                        'delivery_qty': line.qty_delivered,
                        'price_before': line.price_unit,
                        'sale_line_id' : line.id,
                    }))
        self.rma_order_line_ids = order_lines_data

    def open_return_refund_replace_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('sr_customer_supplier_rma.action_return_refund_replace_form')
        return action

    def action_submit(self):
        if not all(line.return_qty > 0 for line in self.rma_order_line_ids):
            raise ValidationError(_("Please select at least one return item to proceed"))

        self.state = 'submit'

    def action_approve(self):
        if self.rma_order_line_ids:
            with_return_ids = self.rma_order_line_ids.filtered(lambda r: r.return_id.reason_action == 'refund_with_return_item')
            without_return_ids = self.rma_order_line_ids.filtered(lambda r: r.return_id.reason_action == 'refund_without_return_item')
            picking_list = []

            if self.company_id and self.company_id.picking_type_id:
                with_picking_type_id = self.company_id.picking_type_id.id
            else:
                with_picking_type_id = False

            if with_picking_type_id and with_return_ids and self.stock_picking_id:
                picking = self.env['stock.picking'].create({
                    'partner_id' : self.sale_order_id.partner_id.id,
                    'location_id': self.stock_picking_id.picking_type_id.default_location_src_id.id,
                    'picking_type_id': with_picking_type_id,
                    'origin': self.sale_order_id.name,
                    'sale_id': self.sale_order_id.id,
                    'rma_order_id': self.id,
                    'move_ids': [(0, 0, {
                        'product_id': return_id.product_id.id,
                        'name': return_id.product_id.display_name,
                        'product_uom_qty': return_id.return_qty,
                        'location_id' : self.stock_picking_id.picking_type_id.default_location_src_id.id,
                        'sale_line_id': return_id.sale_line_id.id,
                    }) for return_id in with_return_ids]
                })
                if picking:
                    picking.action_confirm()
                    picking_list.append(picking.id)

            if self.company_id and self.company_id.picking_type_id:
                without_picking_type_id = self.company_id.without_picking_type_id.id
            else:
                without_picking_type_id = False

            if without_picking_type_id and without_return_ids:
                without_picking_id = self.env['stock.picking'].create({
                    'partner_id': self.sale_order_id.partner_id.id,
                    'location_id': self.stock_picking_id.picking_type_id.default_location_src_id.id,
                    'picking_type_id': without_picking_type_id,
                    'origin': self.sale_order_id.name,
                    'sale_id': self.sale_order_id.id,
                    'rma_order_id': self.id,
                    'move_ids': [(0, 0, {
                        'product_id': return_id.product_id.id,
                        'name' : return_id.product_id.display_name,
                        'product_uom_qty': return_id.return_qty,
                        'location_id': self.stock_picking_id.picking_type_id.default_location_src_id.id,
                        'sale_line_id': return_id.sale_line_id.id,
                    }) for return_id in without_return_ids]
                })
                if without_picking_id:
                    without_picking_id.action_confirm()
                    picking_list.append(without_picking_id.id)
            if picking_list:
                self.picking_ids = [(6, 0, picking_list)]

        self.state = 'approved'

    def button_reject(self):
        self.state = 'reject'

    def action_move_to_draft(self):
        self.state = 'draft'

    def action_validate(self):
        if self.picking_ids and any(picking.state != 'done' for picking in self.picking_ids):
            raise ValidationError(_("You can't proceed until all related stock pickings are in 'Done' state."))

        line_list = []
        if self.rma_replaced_product_ids:
            for line in self.rma_replaced_product_ids:
                line_list.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.qty,
                    'price_unit' : line.price,
                }))

            sale_id = self.env['sale.order'].create({
                'partner_id': self.sale_order_id.partner_id.id,
                'rma_order_id': self.id,
                'order_line': line_list
            })
            if sale_id:
                sale_id.action_confirm()
                existing_orders = self.sale_order_ids.ids or []
                updated_sale_ids = list(set(existing_orders + [sale_id.id]))
                self.sale_order_ids = [(6, 0, updated_sale_ids)]

        self.is_validate = True

    def action_close(self):
        self.state = 'close'

    def action_send_rma(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'RMA Order Email',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_model': 'rma.order',
                'default_rma_ids': self.id,
            }
        }

    def action_create_supplier_rma(self):
        if not all(line.return_qty > 0 for line in self.rma_order_line_ids):
            raise ValidationError(_("Please select at least one return item to proceed"))

        order_lines_data = []
        if self.rma_order_line_ids:
            for line in self.rma_order_line_ids:
                order_lines_data.append((0, 0, {
                    'product_id': line.product_id.id,
                    'delivery_qty': line.delivery_qty,
                    'return_qty': line.return_qty,
                    'price' : line.price_before,
                }))

        supplier_id = self.env['rma.supplier'].create({
            'company_id' : self.company_id.id,
            'subject' : self.subject,
            'rma_main_id' : self.id,
            'date' : self.date,
            'deadline' : self.deadline,
            'priority': self.priority,
            'stock_picking_id' : self.stock_picking_id.id,
            'delivery_partner_id' : self.delivery_partner_id.id,
            'delivery_email' : self.delivery_email,
            'delivery_phone' : self.delivery_phone,
            'rma_notes' : self.rma_notes,
            'rma_supplier_line_ids' : order_lines_data,
        })
        if supplier_id:
            self.state = 'supplier_rma'

    def action_view_receipt(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        return action

    def action_view_refund_invoice(self):
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice")
        action['domain'] = [('id', 'in', self.invoice_ids.ids)]
        return action

    def action_view_sale_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['domain'] = [('id', 'in', self.sale_order_ids.ids)]
        return action

    def action_supplier_rma(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sr_customer_supplier_rma.action_rma_supplier")
        action['domain'] = [('rma_main_id', '=', self.id)]
        return action