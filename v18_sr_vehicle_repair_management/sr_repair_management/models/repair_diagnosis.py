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


class RepairDiagnosis(models.Model):
    _name = "repair.diagnosis"
    _description = "Repair Diagnosis"
    _inherit = ['mail.thread']
    _rec_name = "name"

    name = fields.Char('Name', required=True, default='New', tracking=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', copy=False, tracking=True)
    mobile = fields.Char("Mobile", copy=False, tracking=True)
    email = fields.Char("Email", copy=False, tracking=True)
    date = fields.Date("Date", copy=False, tracking=True, default=fields.Datetime.now, required=True)
    received_user_id = fields.Many2one("res.users", string="Received User", tracking=True, default=lambda self: self.env.uid, required=True)

    vehicle_name = fields.Char("Vehicle Name", copy=False, tracking=True)
    brand = fields.Char("Brand", copy=False, tracking=True)
    model = fields.Char("Model", copy=False, tracking=True)
    color = fields.Char("Color", copy=False, tracking=True)
    license_no = fields.Char("Licence/Plate No.", copy=False, tracking=True)
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', copy=False, tracking=True)
    chassis_number = fields.Char("Chassis Number", copy=False, tracking=True)

    checklist_ids = fields.One2many("repair.checklist", "diagnosis_id", copy=False, tracking=True)
    repair_estimate_ids = fields.One2many("repair.estimate", "diagnosis_id", copy=False, tracking=True)
    total = fields.Float('Estimate Cost', compute='_compute_total', store=True)

    note = fields.Text("Repair Note", copy=False, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('in_workorder', 'In WorkOrder'),
        ('done', 'Done'),
    ], default='draft', copy=False, tracking=True)

    repair_id = fields.Many2one('vehicle.repair.order', copy=False, tracking=True)
    sale_order_ids = fields.Many2many('sale.order', 'sale_diagnosis_rel', 'diagnosis_id', 'order_id', string="Sale Orders", readonly=True, copy=False, tracking=True)
    est_delivery_date = fields.Date("Estimate Delivery Date", copy=False, tracking=True)
    repair_work_order_ids = fields.Many2many('repair.work.order', string="Repair Work Order", readonly=True, copy=False, tracking=True)

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

    work_order_count = fields.Integer(
        string='Work Order Count',
        compute='_compute_work_order_count',
        tracking=True
    )

    so_type = fields.Selection(
        [('in_diagnosis', 'In Diagnosis'), ('in_work_order', 'In Work Order')],
        string="Sale Order Type",
        compute="_compute_so_type",
        store=False
    )

    @api.depends()
    def _compute_so_type(self):
        IrConfigParam = self.env['ir.config_parameter'].sudo()
        so_type = IrConfigParam.get_param('sr_repair_management.so_type', default='in_diagnosis')
        for rec in self:
            rec.so_type = so_type

    @api.depends('repair_estimate_ids.sub_total')
    def _compute_total(self):
        for record in self:
            record.total = sum(est.sub_total for est in record.repair_estimate_ids)

    @api.depends('repair_id')
    def _compute_repair_count(self):
        for record in self:
            record.repair_count = 1 if record.repair_id else 0

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = len(record.sale_order_ids)

    @api.depends('repair_work_order_ids')
    def _compute_work_order_count(self):
        for record in self:
            record.work_order_count = len(record.repair_work_order_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.diagnosis') or "New"
        return super().create(vals_list)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.mobile = self.partner_id.mobile
            self.email = self.partner_id.email

    def action_confirm(self):
        self.state = 'confirm'

    def create_quotations(self):
        for record in self:
            if not all(cl.state == 'done' for cl in record.checklist_ids):
                raise ValidationError("All checklist items must be done before marking this record create as quotation.")

            if not record.partner_id:
                raise UserError("Please select a customer before creating a quotation.")

            if not record.repair_estimate_ids:
                raise UserError("No any estimate found to create a quotation.")

            order_vals = {
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'note': "Generated from Vehicle Diagnosis",
                'diagnosis_id' : record.id,
                'order_line': [],
            }

            order_lines = []
            for part in record.repair_estimate_ids:
                if not part.product_id:
                    continue
                line_vals = (0, 0, {
                    'product_id': part.product_id.id,
                    'product_uom_qty': part.quantity,
                    'price_unit': part.price or part.product_id.list_price,
                    'name': part.product_id.display_name,
                })
                order_lines.append(line_vals)

            order_vals['order_line'] = order_lines

            sale_order = self.env['sale.order'].create(order_vals)
            record.sale_order_ids = [(6, 0, [sale_order.id])]

            for estimate in record.repair_estimate_ids:
                estimate.sale_order_id = sale_order
                if estimate.vehicle_spare_parts_id:
                    estimate.vehicle_spare_parts_id.sale_order_id = sale_order

    def create_work_order(self):
        if not self.checklist_ids:
            raise UserError("Please add at least one checklist item before creating a work order.")

        action = self.env['ir.actions.actions']._for_xml_id('sr_repair_management.action_assign_technician_wizard')
        return action

    def create_work_order_records(self):
        work_order_list = []
        for diagnosis in self:
            if not diagnosis.checklist_ids:
                raise UserError("Please add at least one checklist item before creating a work order.")

            for checklist in diagnosis.checklist_ids:
                work_order_id = self.env['repair.work.order'].create({
                    'partner_id': diagnosis.partner_id.id,
                    'checklist_id': checklist.id,
                    'diagnosis_id': diagnosis.id,
                    'description': checklist.description,
                    'attachment_ids': [(6, 0, checklist.attachment_ids.ids)],
                    'vehicle_name': diagnosis.vehicle_name,
                    'brand': diagnosis.brand,
                    'model': diagnosis.model,
                    'color': diagnosis.color,
                    'license_no': diagnosis.license_no,
                    'fuel_type': diagnosis.fuel_type,
                    'chassis_number': diagnosis.chassis_number,
                    'user_id' : checklist.user_id.id,
                    'note' : diagnosis.note,
                })
                work_order_list.append(work_order_id.id)

            diagnosis.write({
                'state' : 'in_workorder',
                'repair_work_order_ids' : [(6, 0, work_order_list)],
            })
            diagnosis.added_spare_parts_work_order()

    def added_spare_parts_work_order(self):
        for record in self.repair_estimate_ids:
            workorders = self.env['repair.work.order'].search([
                ('checklist_id', '=', record.checklist_id.id),
                ('diagnosis_id', '=', record.diagnosis_id.id),
            ])
            for order in workorders:
                existing_part = self.env['vehicle.spare.parts'].search([
                    ('repair_work_order_id', '=', order.id),
                    ('repair_estimate_id', '=', record.id),
                ])
                if not existing_part:
                    spare_parts_id = self.env['vehicle.spare.parts'].create({
                        'product_id': record.product_id.id,
                        'quantity': record.quantity,
                        'price': record.price,
                        'notes': record.notes,
                        'repair_work_order_id': order.id,
                        'repair_estimate_id': record.id,
                        'diagnosis_id': record.diagnosis_id.id,
                    })
                    record.write({
                        'repair_work_order_id' : order.id,
                        'vehicle_spare_parts_id' : spare_parts_id.id,
                    })

    def action_done(self):
        if not all(cl.state == 'done' for cl in self.checklist_ids):
            raise ValidationError("All checklist items must be done before marking this record as done.")

        if self.so_type == 'in_diagnosis':
            if not self.sale_order_ids:
                raise ValidationError("Please select a Sale Order before proceeding.")
            if not self.sale_order_ids.invoice_ids:
                raise ValidationError(
                    "No invoice has been created for the selected Sale Order. Please create an invoice first.")

        self.state = 'done'
        self.repair_id.state = 'done'

    def write(self, vals):
        result = super(RepairDiagnosis, self).write(vals)
        if 'repair_estimate_ids' in vals and vals['repair_estimate_ids']:
            self.added_spare_parts_work_order()
        return result

    def action_view_repair(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicle Repair Form',
            'res_model': 'vehicle.repair.order',
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
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
            'target': 'current',
        }

    def action_view_work_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repair Work Order',
            'res_model': 'repair.work.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.repair_work_order_ids.ids)],
            'target': 'current',
        }
