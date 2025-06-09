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


class RepairDetails(models.Model):
    _name = "repair.details"
    _description = "Repair Details"
    _inherit = ['mail.thread']
    _rec_name = "name"

    repair_id = fields.Many2one('vehicle.repair.order')
    name = fields.Char('Name', required=True, tracking=True)
    description = fields.Text("Description", copy=False, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Images")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_diagnosis', 'In Diagnosis'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='draft', copy=False, tracking=True)
    diagnosis_id = fields.Many2one('repair.diagnosis', string="Diagnosis")
    checklist_id = fields.Many2one('repair.checklist', string="Checklist")
