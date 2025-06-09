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
from odoo.exceptions import UserError, ValidationError

FUEL_TYPES = [
    ('diesel', 'Diesel'),
    ('gasoline', 'Gasoline'),
    ('full_hybrid', 'Full Hybrid'),
    ('plug_in_hybrid_diesel', 'Plug-in Hybrid Diesel'),
    ('plug_in_hybrid_gasoline', 'Plug-in Hybrid Gasoline'),
    ('cng', 'CNG'),
    ('lpg', 'LPG'),
    ('hydrogen', 'Hydrogen'),
    ('electric', 'Electric'),
]


class CarDiagnosis(models.Model):
    _name = "car.diagnosis"
    _description = "Car Diagnosis"
    _inherit = ['mail.thread']
    _rec_name = "name"

    name = fields.Char('Name', required=True, default='New', tracking=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', copy=False, tracking=True)
    mobile = fields.Char("Mobile", copy=False, tracking=True)
    email = fields.Char("Email", copy=False, tracking=True)
    date = fields.Date("Date", copy=False, tracking=True, default=fields.Datetime.now, required=True)
    received_user_id = fields.Many2one("res.users", string="Received User", tracking=True, default=lambda self: self.env.uid, required=True)
    user_id = fields.Many2one("res.users", string="Technician", tracking=True)

    car_name = fields.Char("Car Name", copy=False, tracking=True)
    brand = fields.Char("Brand", copy=False, tracking=True)
    model = fields.Char("Model", copy=False, tracking=True)
    color = fields.Char("Color", copy=False, tracking=True)
    license_no = fields.Char("Licence/Plate No.", copy=False, tracking=True)
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', copy=False, tracking=True)
    chassis_number = fields.Char("Chassis Number", copy=False, tracking=True)

    checklist_ids = fields.One2many("car.repair.checklist", "diagnosis_id", copy=False, tracking=True)
    spare_parts_ids = fields.One2many("car.spare.parts", "diagnosis_id", copy=False, tracking=True)

    note = fields.Text("Repair Note", copy=False, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='draft', copy=False, tracking=True)

    repair_id = fields.Many2one('car.repair.form', copy=False, tracking=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True, copy=False, tracking=True)

    repair_count = fields.Integer(
        string='Repair Count',
        compute='_compute_repair_count',
        tracking=True
    )

    sale_order_count = fields.Integer(
        string='Sale Order Count',
        compute='_compute_sale_order_count',
        tracking=True
    )

    @api.depends('repair_id')
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = 1 if record.repair_id else 0

    @api.depends('sale_order_id')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = 1 if record.sale_order_id else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('car.diagnosis') or "New"
        return super().create(vals_list)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.mobile = self.partner_id.mobile
            self.email = self.partner_id.email

    def action_confirm(self):
        if not self.user_id:
            raise ValidationError(_("Please assign Technician"))
        self.state = 'confirm'

    # def assign_technician(self):
    #     action = self.env['ir.actions.actions']._for_xml_id('sr_car_repair_management.action_assign_technician_wizard')
    #     return action

    def create_quotations(self):
        for record in self:
            if not record.partner_id:
                raise UserError("Please select a customer before creating a quotation.")

            if not record.spare_parts_ids:
                raise UserError("No spare parts found to create a quotation.")

            # Create the sale order
            order_vals = {
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'note': "Generated from Car Diagnosis",
                'diagnosis_id' : record.id,
                'order_line': [],
            }

            order_lines = []
            for part in record.spare_parts_ids:
                if not part.product_id:
                    continue
                line_vals = (0, 0, {
                    'product_id': part.product_id.id,
                    'product_uom_qty': part.quantity,
                    'price_unit': part.price or part.product_id.list_price,
                    'name': part.name or part.product_id.name,
                })
                order_lines.append(line_vals)

            order_vals['order_line'] = order_lines

            sale_order = self.env['sale.order'].create(order_vals)
            record.sale_order_id = sale_order.id

    def action_done(self):
        if not self.sale_order_id:
            raise ValidationError("Please select a Sale Order before proceeding.")
        if not self.sale_order_id.invoice_ids:
            raise ValidationError(
                "No invoice has been created for the selected Sale Order. Please create an invoice first.")

        self.state = 'done'
        self.repair_id.state = 'done'

    def action_view_repair(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Car Repair Form',
            'res_model': 'car.repair.form',
            'view_mode': 'form',
            'res_id': self.repair_id.id,
            'target': 'current',
        }

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'target': 'current',
        }