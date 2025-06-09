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


class RepairWorkOrder(models.Model):
    _name = 'repair.work.order'
    _inherit = ['mail.thread']
    _description = 'Repair Work Order'
    _rec_name = 'name'

    name = fields.Char('Name', required=True, default='New',readonly=True)
    partner_id = fields.Many2one('res.partner',string='Customer',required=True,copy=False)
    checklist_id = fields.Many2one('repair.checklist',string='CheckList',required=True,copy=False)
    diagnosis_id = fields.Many2one('repair.diagnosis',string='Diagnosis',copy=False)
    spar_parts_ids = fields.One2many('vehicle.spare.parts','repair_work_order_id','Spar Parts',copy=False)
    vehicle_name = fields.Char("Vehicle Name", copy=False, tracking=True)
    brand = fields.Char("Brand", copy=False, tracking=True)
    model = fields.Char("Model", copy=False, tracking=True)
    color = fields.Char("Color", copy=False, tracking=True)
    license_no = fields.Char("Licence/Plate No.", copy=False, tracking=True)
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', copy=False, tracking=True)
    chassis_number = fields.Char("Chassis Number", copy=False, tracking=True)
    description = fields.Text("Description", copy=False, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Images")
    user_id = fields.Many2one("res.users", string="Technician", tracking=True)
    worked_hours = fields.Float("Worked Hours", tracking=True)
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True, copy=False, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ], default='draft', copy=False, tracking=True)
    note = fields.Text("Repair Note", copy=False, tracking=True)

    sale_order_count = fields.Integer(
        string='Sale Order Count',
        compute='_compute_sale_order_count',
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

    @api.depends('sale_order_id')
    def _compute_sale_order_count(self):
        for record in self:
            record.sale_order_count = 1 if record.sale_order_id else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('repair.work.order') or "New"
        return super().create(vals_list)

    def create_quotations(self):
        for record in self:
            if not record.partner_id:
                raise UserError("Please select a customer before creating a quotation.")

            if not record.spar_parts_ids:
                raise UserError("No any spar parts found to create a quotation.")

            order_vals = {
                'partner_id': record.partner_id.id,
                'origin': record.name,
                'note': "Generated from Vehicle Diagnosis",
                'repair_work_order_id' : record.id,
                'order_line': [],
            }

            order_lines = []
            for part in record.spar_parts_ids:
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
            record.sale_order_id = sale_order.id

            if record.diagnosis_id:
                record.diagnosis_id.sale_order_ids = [(4, sale_order.id)]

            for line in record.spar_parts_ids:
                line.sale_order_id = sale_order.id
                if line.repair_estimate_id:
                    line.repair_estimate_id.sale_order_id = sale_order.id

    def button_confirm(self):
        if not self.user_id:
            raise ValidationError(_("Please assign Technician"))
        self.state = 'in_progress'
        self.checklist_id.state = 'in_progress'
        if self.checklist_id.repair_details_id:
            self.checklist_id.repair_details_id.state = 'in_progress'

    def button_finished(self):
        if self.worked_hours <= 0:
            raise ValidationError(_("Please set worked hours"))

        if self.so_type == 'in_work_order':
            if not self.sale_order_id:
                raise ValidationError("Please select a Sale Order before proceeding.")
            if not self.sale_order_id.invoice_ids:
                raise ValidationError(
                    "No invoice has been created for the selected Sale Order. Please create an invoice first.")

        self.state = 'finished'
        self.checklist_id.state = 'done'
        if self.checklist_id.repair_details_id:
            self.checklist_id.repair_details_id.state = 'done'

    def action_view_diagnosis(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Diagnosis',
            'res_model': 'repair.diagnosis',
            'view_mode': 'list,form',
            'domain': [('id', '=', self.diagnosis_id.id)],
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
