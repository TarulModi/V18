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


class RepairChecklist(models.Model):
    _name = "repair.checklist"
    _description = "Repair Checklist"
    _inherit = ['mail.thread']
    _rec_name = "name"

    repair_id = fields.Many2one('vehicle.repair.order')
    repair_details_id = fields.Many2one('repair.details')
    diagnosis_id = fields.Many2one('repair.diagnosis')
    name = fields.Char('Name', required=True, tracking=True)
    description = fields.Text("Description", copy=False, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Images")
    user_id = fields.Many2one("res.users", string="Technician")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='draft', copy=False, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super(RepairChecklist, self).create(vals_list)
        for record in records:
            if not record.repair_details_id and record.diagnosis_id and record.diagnosis_id.repair_id:
                repair_details = self.env['repair.details'].create({
                    'repair_id': record.diagnosis_id.repair_id.id,
                    'diagnosis_id': record.diagnosis_id.id,
                    'name': record.name,
                    'description': record.description,
                    'attachment_ids': [(6, 0, record.attachment_ids.ids)],
                    'state': 'in_diagnosis',
                    'checklist_id': record.id,
                })

                record.write({
                    'repair_details_id': repair_details.id,
                    'repair_id': repair_details.repair_id.id,
                })
        return records