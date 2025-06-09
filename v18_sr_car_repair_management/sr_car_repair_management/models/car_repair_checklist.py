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


class CarRepairChecklist(models.Model):
    _name = "car.repair.checklist"
    _description = "Car Repair Checklist"
    _inherit = ['mail.thread']
    _rec_name = "name"

    repair_id = fields.Many2one('car.repair.form')
    diagnosis_id = fields.Many2one('car.diagnosis')
    name = fields.Char('Name', required=True, tracking=True)
    description = fields.Text("Description", copy=False, tracking=True)
    attachment_ids = fields.Many2many('ir.attachment', string="Images")