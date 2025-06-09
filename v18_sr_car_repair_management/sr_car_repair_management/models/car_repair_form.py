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


class CarRepairForm(models.Model):
    _name = "car.repair.form"
    _description = "Car Repair Form"
    _inherit = ['mail.thread']
    _rec_name = "name"

    name = fields.Char('Name', required=True, default='New', tracking=True, readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', copy=False, tracking=True)
    mobile = fields.Char("Mobile", copy=False, tracking=True)
    email = fields.Char("Email", copy=False, tracking=True)
    date = fields.Date("Date", copy=False, tracking=True, default=fields.Datetime.now, required=True)
    received_user_id = fields.Many2one("res.users", string="Received User", tracking=True, default=lambda self: self.env.uid, required=True)

    car_name = fields.Char("Car Name", copy=False, tracking=True)
    brand = fields.Char("Brand", copy=False, tracking=True)
    model = fields.Char("Model", copy=False, tracking=True)
    color = fields.Char("Color", copy=False, tracking=True)
    license_no = fields.Char("Licence/Plate No.", copy=False, tracking=True)
    fuel_type = fields.Selection(FUEL_TYPES, 'Fuel Type', copy=False, tracking=True)
    chassis_number = fields.Char("Chassis Number", copy=False, tracking=True)

    checklist_ids = fields.One2many("car.repair.checklist", "repair_id", copy=False, tracking=True)

    note = fields.Text("Repair Note", copy=False, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('in_diagnosis', 'In Diagnosis'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ], default='draft', copy=False, tracking=True)

    diagnosis_id = fields.Many2one('car.diagnosis', copy=False, tracking=True)
    diagnosis_count = fields.Integer(
        string='Diagnosis Count',
        compute='_compute_diagnosis_count',
        tracking=True
    )

    @api.depends('diagnosis_id')
    def _compute_diagnosis_count(self):
        for record in self:
            seach_count = self.env['car.diagnosis'].search_count([('id', '=', self.diagnosis_id.id)])
            record.diagnosis_count = seach_count

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('car.repair.form') or "New"
        return super().create(vals_list)

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.mobile = self.partner_id.mobile
            self.email = self.partner_id.email

    def action_confirm(self):
        self.state = 'confirm'

    def create_diagnosis(self):
        if not self.checklist_ids:
            raise ValidationError(_("Please add checklist details."))
        self.ensure_one()

        diagnosis_vals = {
            'partner_id': self.partner_id.id,
            'mobile': self.mobile,
            'email': self.email,
            'date': self.date,
            'received_user_id': self.received_user_id.id,
            'car_name': self.car_name,
            'brand': self.brand,
            'model': self.model,
            'color': self.color,
            'license_no': self.license_no,
            'fuel_type': self.fuel_type,
            'chassis_number': self.chassis_number,
            'note': self.note,
            'repair_id': self.id,
            'checklist_ids': [
                (0, 0, {
                    # 'repair_id': checklist.repair_id.id,
                    'name': checklist.name,
                    'description': checklist.description,
                    'attachment_ids': [(6, 0, checklist.attachment_ids.ids)],
                }) for checklist in self.checklist_ids
            ]
        }

        diagnosis = self.env['car.diagnosis'].create(diagnosis_vals)
        if diagnosis:
            self.write({
                'state': 'in_diagnosis',
                'diagnosis_id' : diagnosis.id,
            })

    # def action_done(self):
    #     self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_reset_to_draft(self):
        self.state = 'draft'

    def action_view_diagnosis(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Diagnosis',
            'res_model': 'car.diagnosis',
            'view_mode': 'form',
            'res_id': self.diagnosis_id.id,
            'target': 'current',
        }